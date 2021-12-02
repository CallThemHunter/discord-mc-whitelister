from config import *
from typing import List
if isSFTPEnabled:
    from sftpInterface import (
        appendExceptTrue
    )
else:
    from localInterface import (
        appendExceptTrue
    )


# for link and requestlist
def removeFromUIDNameListByUserID(filename: str, userID: int):
    with open(filename, "r") as f:
        lines: List[str] = f.readlines()
    lines_split: List[List[str]] = list(map(lambda line: line.split(" "), lines))

    lines_bool: List[bool] = list(map(lambda line_list: line_list[0] == str(userID), lines_split))

    return appendExceptTrue(filename, lines, lines_bool)


# for link and request list
def removeFromUIDNameListByMCName(filename: str, mcName: str):
    with open(filename, "r") as f:
        lines: List[str] = f.readlines()
    lines_split: List[List[str]] = list(map(lambda line: line.split(" "), lines))

    lines_bool: List[bool] = list(map(lambda line_list: line_list[1] == mcName, lines_split))

    return appendExceptTrue(filename, lines, lines_bool)


# for whitelist
def removeFromNameList(filename: str, mcName: str):
    with open(filename, "r") as f:
        lines: List[str] = f.readlines()

    lines_bool: List[bool] = list(map(lambda line: line == mcName, lines))

    return appendExceptTrue(filename, lines, lines_bool)


# for deny list
def removeFromUIDList(filename: str, userID: int):
    with open(filename, "r") as f:
        lines: List[str] = f.readlines()

    lines_bool: List[bool] = list(map(lambda line: line == str(userID), lines))

    return appendExceptTrue(filename, lines, lines_bool)
