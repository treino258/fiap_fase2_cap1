from enum import StrEnum
from datetime import datetime

from src.database.logger.color_text import makeRed, makeYellow, makeBlue, makeCyan, makeMagenta, makeGreen


class LEVEL(StrEnum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"
    CRITICAL = "critical"
    SUCCESS = "success"

    def name(self):
        return self.value.upper()


def log(message: str, level: LEVEL, *, time:datetime|None = None, silent:bool = False, write:bool = True) -> None:

    now = time or datetime.now()

    logmessage = f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] [{level.name()}] {message}"

    if not silent:
        match level:
            case LEVEL.ERROR:
                print(makeRed(logmessage))

            case LEVEL.WARNING:
                print(makeYellow(logmessage))

            case LEVEL.INFO:
                print(makeBlue(logmessage))

            case LEVEL.DEBUG:
                print(makeCyan(logmessage))

            case LEVEL.CRITICAL:
                print(makeMagenta(logmessage))

            case LEVEL.SUCCESS:
                print(makeGreen(logmessage))

            case _:
                raise NotImplemented(f"Level {level} not implemented")
    if write:
        with open("log.txt", "a") as f:
            f.write(logmessage + "\n")


def log_error(message: str, *, time:datetime|None = None, silent:bool = False, write:bool = True) -> None:
    log(message, LEVEL.ERROR, time=time, silent=silent, write=write)

def log_warning(message: str, *, time:datetime|None = None, silent:bool = False, write:bool = True) -> None:
    log(message, LEVEL.WARNING, time=time, silent=silent, write=write)

def log_info(message: str, *, time:datetime|None = None, silent:bool = False, write:bool = True) -> None:
    log(message, LEVEL.INFO, time=time, silent=silent, write=write)

def log_debug(message: str, *, time:datetime|None = None, silent:bool = False, write:bool = True) -> None:
    log(message, LEVEL.DEBUG, time=time, silent=silent, write=write)

def log_critical(message: str, *, time:datetime|None = None, silent:bool = False, write:bool = True) -> None:
    log(message, LEVEL.CRITICAL, time=time, silent=silent, write=write)

def log_success(message: str, *, time:datetime|None = None, silent:bool = False, write:bool = True) -> None:
    log(message, LEVEL.SUCCESS, time=time, silent=silent, write=write)