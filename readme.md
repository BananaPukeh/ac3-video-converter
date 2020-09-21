# AC3 Video Converter
This is a tool for automatically converting your media library to AC3 or EAC3 audio codec. It uses FFMPEG to convert the files.

## Features
- Convert `AAC` to `AC3`
- Convert `DTS`, `DTS-HD` and `HE-AAC` to `EAC3`
- Converts all audio tracks in the file
- Keeps all subtitles
- Add multiple library paths (see below)
- Telegram notifications

# Installation

```
docker run -d \
--name ac3-converter \
-v /path/to/tvshows:/library/tvshows \
-v /path/to/movies:/library/movies \
-e libraries="/library/tvshows;/library/movies" \
--restart unless-stopped \
rutgernijhuis/ac3-video-converter
```

In the above command there are two libraries mounted. On the host the library `/path/to/tvshows/` is the location where the media lives, this is mapped to `/library/tvshows` in the container. You can add as many libraries as you want, but you need to specify the mapped paths in the environment variable `libraries` delimitted by a semicolon: (`;`) as shown.

## Environment variables
| Variable         | Required | Default | Usage                                                         |
|------------------|----------|---------|---------------------------------------------------------------|
| libraries        | Yes      | ""      | Specify all mapped library paths delimited by a semicolon     |
| interval         | No       | 3600    | Scan interval in seconds                                      |
| replace_original | No       | true    | Should the original file be replaced? Mostly used for testing |
| telegram_token   | No       | ""      | Telegram bot token                                            |
| telegram_chat_id | No       | ""      | Telegram chat id                                              |

# Running it locally
If you want to run it locally, I suppose you know what you are doing.

Tested on Python 3.8.5

`pip install -r requirements.txt`

Note Before running:

The script uses environment variables to locate your library, interval time and other settings. Make sure the script can find them.
For testing purposes it is reccomended to use `./demo_libraries/movies;./demo_libraries/shows` as value for `libraries` with your own content.
I used VSCode for developing and added them to `./vscode/launch.json`
