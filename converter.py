import os
from pathlib import Path
import ffmpeg
import subprocess
import shutil
import requests
import time

# Paths splitted by semicolon
libraries = os.getenv("libraries")
validExtensions = [".mkv", ".mp4", ".m4v"]
desiredCodecs = ["ac3", "eac3", "truehd"]
interval = int(os.getenv('interval', "3600"))

# Usefull for testing purposes
replaceOriginal = os.getenv("replace_original", "true") == "true"


def scanLibraries():
    paths = libraries.split(';')

    for path in paths:
        scanFolder(path)


def scanFolder(path):
    for f in os.listdir(path):
        subPath = os.path.join(path, f)
        if os.path.isdir(subPath):
            # Repeat recusively
            scanFolder(subPath)
        else:
            checkFile(subPath)


def checkFile(path):
    extension = Path(path).suffix
    if extension in validExtensions:
        # Check if this file needs converting

        try:
            probeRes = ffmpeg.probe(path)
            for stream in probeRes["streams"]:
                if stream["codec_type"] == "audio":
                    if stream["channels"] > 2 or True:  # Disabled for now
                        # print("More than two channels found!")
                        codecName = stream["codec_name"]
                        if not codecName in desiredCodecs:
                            if codecName == "aac":
                                newCodec = "ac3"
                            elif codecName == "he-aac":
                                newCodec = "eac3"
                            elif codecName == "dts":
                                newCodec = "eac3"
                            elif codecName == "opus":
                                newCodec = "eac3"
                            elif codecName == "flac":
                                newCodec = "eac3"
                            else:
                                print("Error, don't know how to re-encode %s" %
                                      codecName)
                                notify(
                                    "❌ Error don't know how to re-encode *{}* for:```{}```".format(codecName, path))

                            if not newCodec == None:
                                reencode(path, newCodec, codecName)
                                # Break so this file wont trigger twice if multiple audio tracks
                                break
        except:
            print("Failed to probe {}".format(path))


def reencode(path, newCodec, oldCodec):
    print("Start re-encoding from {} to {} for {} ".format(oldCodec, newCodec, path))

    FFMPEG_PATH = "ffmpeg"

    folder = os.path.dirname(path)
    fileName = Path(path).stem
    outputPath = os.path.join(folder, "converted.mkv")

    # notify(" Start re-encoding *{}* to *{}*```{}```".format(oldCodec, newCodec, fileName))

    startTime = time.time()
    # Go with an direct subprocess because the python-ffmpeg api is kindoff vague
    command = [
        FFMPEG_PATH,
        "-y",  # Overwrite if exists
        "-i",  # Specify input
        path,
        "-c:v",  # Passthru video
        "copy",
        "-c:a",  # Convert only audio
        newCodec,
        "-map",
        "0",  # Map all audio streams
        outputPath,
    ]

    subprocess.call(command)

    if not os.path.exists(outputPath):
        notify("❌ Failed to convert!")

    if Path(outputPath).stat().st_size == 0:
        notify("❌ Output file is empty, conversion failed")
    else:
        # Replace original file
        if replaceOriginal:
            shutil.move(outputPath, path)
        else:
            newPath = os.path.join(
                folder, fileName + " - {}.mkv".format(newCodec.upper()))
            shutil.move(outputPath, newPath)

        duration = int(time.time() - startTime)

        notify("⚡ Re-encoded *{}* to *{}* in {} sec```{}```".format(oldCodec,
                                                                    newCodec, duration, fileName.replace("/", "-")))


def notify(message):
    bot_token = os.getenv("telegram_token", "")
    bot_chatID = os.getenv("telegram_chat_id", "")

    if not bot_token == "" and not bot_chatID == "":
        send_text = 'https://api.telegram.org/bot' + bot_token + \
            '/sendMessage?disable_notification=true&chat_id=' + \
            bot_chatID + '&parse_mode=Markdown&text=' + message

        _ = requests.get(send_text)


# Start
print("Start monitoring library for unwanted audio codecs")
print("Interval time {} seconds".format(interval))

notify("🆗 Start monitoring library for unwanted audio codec.\nRunning at: `{} seconds`".format(interval))
while True:
    scanLibraries()
    time.sleep(interval)
