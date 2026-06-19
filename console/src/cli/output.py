# ==========================================================
# OpenShell Console Output Engine
# ==========================================================


import sys
from datetime import datetime



class Colors:

    RESET="\033[0m"

    BLACK="\033[30m"
    RED="\033[31m"
    GREEN="\033[32m"
    YELLOW="\033[33m"
    BLUE="\033[34m"
    MAGENTA="\033[35m"
    CYAN="\033[36m"
    WHITE="\033[37m"

    BOLD="\033[1m"
    DIM="\033[2m"



class OutputStyle:


    PREFIXES = {

        "info":
            (
                Colors.CYAN,
                "[*]"
            ),

        "success":
            (
                Colors.GREEN,
                "[+]"
            ),

        "warning":
            (
                Colors.YELLOW,
                "[!]"
            ),

        "error":
            (
                Colors.RED,
                "[-]"
            ),

        "debug":
            (
                Colors.MAGENTA,
                "[D]"
            )
    }





class ConsoleOutput:


    def __init__(
        self,
        enable_colors=True
    ):

        self.enable_colors = enable_colors



    def _color(
        self,
        text,
        color
    ):

        if not self.enable_colors:

            return text


        return (
            color +
            text +
            Colors.RESET
        )



    def write(
        self,
        level,
        message
    ):


        color, prefix = (
            OutputStyle.PREFIXES[level]
        )


        timestamp = datetime.now().strftime(
            "%H:%M:%S"
        )


        line = (
            f"{timestamp} "
            f"{prefix} "
            f"{message}"
        )


        print(
            self._color(
                line,
                color
            )
        )



    def info(self,message):

        self.write(
            "info",
            message
        )



    def success(self,message):

        self.write(
            "success",
            message
        )



    def warning(self,message):

        self.write(
            "warning",
            message
        )



    def error(self,message):

        self.write(
            "error",
            message
        )



    def debug(self,message):

        self.write(
            "debug",
            message
        )



    def banner(self,title):

        line="=" * 60


        print(
            self._color(
                line,
                Colors.BLUE
            )
        )


        print(
            self._color(
                title.center(60),
                Colors.BOLD + Colors.BLUE
            )
        )


        print(
            self._color(
                line,
                Colors.BLUE
            )
        )


    def prompt(
        self,
        text="console"
    ):


        if not self.enable_colors:

            return f"{text}> "


        return (
            Colors.BOLD +
            Colors.GREEN +
            text +
            Colors.RESET +
            Colors.BOLD +
            "> " +
            Colors.RESET
        )