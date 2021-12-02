from typing import List

from config import denylist_file, requestlist_file, whitelist_file, discordmclinklist_file


def appendToFile(filename: str, string: str):
    with open(filename, "a") as f:
        f.write("\n" + string)


def appendExceptTrue(filename, lines, lines_bool):
    ret = ""
    while lines_bool.count(True) != 0:
        idx = lines_bool.index(True)
        ret = lines.pop(idx)
        lines_bool.pop(idx)
    with open(filename, "a") as f:
        for line in lines:
            f.write("\n" + line)

    return ret


def load_denylist() -> List[str]:
    with open(denylist_file, "r") as f:
        deny_list: List[str] = f.readlines()
    return deny_list


def load_requestlist() -> List[List[str]]:
    with open(requestlist_file, "r") as f:
        request_list: List[List[str]] = list(map(
            lambda line: line.split(" "), f.readlines()
        ))
    return request_list


def load_whitelist() -> List[str]:
    with open(whitelist_file, "r") as f:
        white_list: List[str] = f.readlines()
    return white_list


def load_linklist() -> List[List[str]]:
    with open(discordmclinklist_file, "r") as f:
        link_list = list(map(
            lambda line: line.split(" "), f.readlines()
        ))
    return link_list