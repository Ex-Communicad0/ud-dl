#!/usr/bin/python3
# pylint: disable=R,C,W,E
import subprocess
from udemy.compat import re, time

from udemy.logger import logger
from udemy.progress import progress


class YTDL:

    _PROGRESS_PATTERN = re.compile(
        r"(Downloading|ETA|Speed)\s*\:\s*(\S+)"
    )

    def __init__(
        self, url, filepath, format_id, quiet=False, callback=lambda *x: None
    ):
        self.url = url
        self.filepath = filepath
        self.quiet = quiet
        self.callback = callback
        self.format_id = format_id

    def _command(self):
        """
        youtube-dl -k -o %(title)s.%(ext)s --force-generic-extractor --fixup never -f "bestvideo,bestaudio" ""
        """
        command = [
            "yt-dlp",
            "--force-generic-extractor", "--allow-unplayable-formats",
            "--downloader", "aria2c", "--fixup", "never", "--concurrent-fragments", "50",
            "-k",
            "-o",
            f"{self.filepath}.%(ext)s",
            "-f",
            self.format_id,
            f"{self.url}"
        ]
        return command

    def download(self):
        retVal = {}
        command = self._command()
        try:
            code = subprocess.Popen(
                command
            ).wait()
            if code == 0:
                retVal = {"status": "True", "msg": "download"}
            else:
                retVal = {
                    "status": "False",
                    "msg": "Error: KeyboardInterrupt",
                }
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        return retVal
