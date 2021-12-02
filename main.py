import discord
from typing import TYPE_CHECKING
from discord import Message
from discord import Member
from discord import Permissions
from discord.ext import commands
from discord.ext.commands import (
    MemberConverter, MessageNotFound, Greedy
)
from typing import TextIO, List, Optional

whitelist_file = "whitelist.txt"
discordmclinklist_file = "discordmclinklist.txt"
denylist_file = "denyuserid.txt"
requestlist_file = "requests.txt"

bot: commands.Bot = commands.Bot(command_prefix='malfbot')
selfWhiteList: bool = False


@bot.command()
async def request(ctx: commands.Context, mcName: str):
    deny_list = load_denylist()
    if str(ctx.author.id) in deny_list:
        await ctx.reply("You have been barred from requesting access,"
                        "contact a mod if you believe this was an error",
                        mention_author=True)
        return

    link_list = load_linklist()
    link_list_ids = list(map(
        lambda line_split: line_split[0], link_list
    ))
    if str(ctx.author.id) in link_list_ids:
        await ctx.reply("You already have an account linked, unlink it"
                        "by using malfbot unlink", mention_author=True)
        return

    if selfWhiteList:
        appendToFile(whitelist_file, mcName)
        await ctx.reply("You have been added to the whitelist. please"
                        "allow a few minutes for the whitelist to reload",
                        mention_author=True)
        return

    # TODO add reacts

    line = str(ctx.author.id) + " " + mcName
    appendToFile(requestlist_file, line)
    await ctx.reply("You have been added to the requests list, you will"
                    "be screened by a mod shortly for server access",
                    mention_author=True)
    return


@bot.command()
@commands.has_permissions(manage_messages=True)
async def approve(ctx: commands.Context):
    if ctx.message.reference is None or ctx.message.is_system():
        await ctx.reply("You must use this in reply to another user's"
                        "message", mention_author=True)
        return

    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    line = removeFromUIDNameListByUserID(requestlist_file, message.author.id)
    appendToFile(discordmclinklist_file, line)
    mcName = line.split(" ")[1]
    appendToFile(whitelist_file, mcName)

    await ctx.send("You have been approved for server access, please"
                   "wait a couple minutes for the whitelist to reload",
                   mention_author=True, reference=message)
    return


@bot.command()
@commands.has_permissions(manage_messages=True)
async def reject(ctx: commands.Context):
    if ctx.message.reference is None or ctx.message.is_system():
        await ctx.send("You must use this in reply to another user's"
                       "message", mention_author=True)
        return

    message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    removeFromUIDNameListByUserID(requestlist_file, message.author.id)

    await ctx.send("You have been denied server access, consult a mod"
                   "regarding this if you believe this is in error",
                   mention_author=False, reference=message)
    return


@bot.command()
async def unlink(ctx: commands.Context, *arg: Optional[MemberConverter]):
    if arg is None:
        user_id = ctx.author.id
        line = removeFromUIDNameListByUserID(discordmclinklist_file, user_id)
        mcName = line.split(" ")[1]

        removeFromNameList(whitelist_file, mcName)

        await ctx.reply("Your account has been unlinked from the server and"
                        "you have been removed from the whitelist, you may"
                        "request access at another point",
                        mention_author=True)
        return

    elif ctx.author.guild_permissions.manage_messages.flag:
        if isinstance(arg, Member):
            user: Member = arg
            line = removeFromUIDNameListByUserID(discordmclinklist_file, user.id)
            mcName = line.split(" ")[1]
            removeFromNameList(whitelist_file, mcName)

            await ctx.reply("This account has been unlinked from the server and"
                            "removed from the whitelist",
                            mention_author=True)
    else:
        await ctx.reply("You are only allowed to use this command as an"
                        "empty message", mention_author=True)
        return


@bot.command()
async def addtodenylist(ctx: commands.Context, arg: str):
    member: Member = MemberConverter().convert(ctx, arg)
    appendToFile(denylist_file, )
    pass


@bot.command()
async def removefromdenylist(ctx: commands.Context):
    pass


@bot.command()
async def overrideadd(ctx: commands.Context):
    pass


@bot.command()
async def banFromWhitelist(ctx: commands.Context, mcname):
    pass


@bot.command()
async def toggleSelfWhitelist(ctx: commands.Context):
    pass


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
