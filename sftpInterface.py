from config import *
from ftpconfig import *
from typing import List
import paramiko
from fileIO import (
    removeFromUIDNameListByUserID,
    removeFromUIDNameListByMCName,
    removeFromNameList,
    removeFromUIDList
)



def create_sftp_client() -> paramiko.SFTPClient:
    transport = paramiko.Transport((host, port))
    transport.connect(None, username, password, key)

    sftp: paramiko.SFTPClient = paramiko.SFTPClient.from_transport(transport)

    return sftp


def readSFTP(filename):
    with create_sftp_client().open(filename, "r") as sftp:
        lines = sftp.readlines

    return lines


def appendToFile(filename: str, string: str):
    with create_sftp_client().open(filename, "a") as sftp:
        sftp.write(string)

    return


def appendExceptTrue(filename, lines, lines_bool):
    pass


def load_denylist() -> List[str]:
    return readSFTP(denylist_file)


def load_requestlist() -> List[List[str]]:
    return readSFTP(requestlist_file)


def load_whitelist() -> List[str]:
    return readSFTP(whitelist_file)


def load_linklist() -> List[List[str]]:
    return readSFTP(discordmclinklist_file)
