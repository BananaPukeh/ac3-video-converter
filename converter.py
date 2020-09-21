import os
from pathlib import Path
import ffmpeg
import subprocess
import shutil

# Paths splitted by semicolon
libraries = os.getenv("libraries")
validExtensions = [".mkv", ".mp4", ".m4v"]
desiredCodecs = ["ac3", "eac3", "truehd"]

# Usefull for testing purposes
replaceOriginal = False


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
        probeRes = ffmpeg.probe(path)
        for stream in probeRes["streams"]:
            if stream["codec_type"] == "audio":
                if stream["channels"] > 2:
                    # print("More than two channels found!")
                    codecName = stream["codec_name"]
                    if not codecName in desiredCodecs:
                        if codecName == "aac":
                            newCodec = "ac3"
                        elif codecName == "he-aac":
                            newCodec = "eac3"
                        elif codecName == "dts":
                            newCodec = "eac3"
                        else:
                            print("Error, don't know how to re-encode %s" %
                                  codecName)
                        reencode(path, newCodec, codecName)
                        # Break so this file wont trigger twice if multiple audio tracks
                        break


def reencode(path, newCodec, oldCodec):
    print("Start re-encoding from {} to {} for {} ".format(oldCodec, newCodec, path))

    FFMPEG_PATH = "ffmpeg"

    folder = os.path.dirname(path)
    fileName = Path(path).stem
    outputPath = os.path.join(folder, "converted.mkv")

    command = [
        FFMPEG_PATH,
        "-y",  # Overwrite if exists
        "-i",  # Specify input
        path,
        "-c:v",  # Passthru video
        "copy",
        "-c:a",  # Convert only audio
        newCodec,
        outputPath,
    ]

    subprocess.call(command)

    # Replace original file
    if replaceOriginal:
        shutil.move(outputPath, path)
    else:
        newPath = os.path.join(
            folder, fileName + " - {}.mkv".format(newCodec.upper()))
        shutil.move(outputPath, newPath)


print("Done running")

# Start
scanLibraries()
