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


def load_denylist() -> List[str]:
    with open("denylist.txt", "r") as f:
        deny_list: List[str] = f.readlines()
    return deny_list


def load_requestlist() -> List[List[str]]:
    with open("requestlist.txt", "r") as f:
        request_list: List[List[str]] = list(map(
            lambda line: line.split(" "), f.readlines()
        ))
    return request_list


def load_whitelist() -> List[str]:
    with open("whitelist.txt", "r") as f:
        white_list: List[str] = f.readlines()
    return white_list


def load_linklist() -> List[List[str]]:
    with open("discordmclink.txt", "r") as f:
        link_list = list(map(
            lambda line: line.split(" "), f.readlines()
        ))
    return link_list
