from discord import Member
from discord.ext import commands
from discord.ext.commands import MemberConverter
from typing import Optional, Coroutine
from fileIO import *
import asyncio

from localInterface import appendToFile, load_denylist, load_linklist

selfWhiteList: bool = False
threadTimerActive: bool = False
timer: Coroutine = None


bot: commands.Bot = commands.Bot(command_prefix='malfbot')


@bot.command()
async def request(ctx: commands.Context, mc_name: str):
    deny_list = load_denylist()
    if str(ctx.author.id) in deny_list:
        await ctx.reply("You have been barred from requesting access,"
                        "contact a mod if you believe this was an error",
                        mention_author=True, delete_after=20)
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
        appendToFile(whitelist_file, mc_name)
        await ctx.reply("You have been added to the whitelist. please"
                        "allow a few minutes for the whitelist to reload",
                        mention_author=True)
        return

    # TODO add reacts

    line = str(ctx.author.id) + " " + mc_name
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
                        "message", mention_author=True, delete_after=20)
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
                       "message", mention_author=True, delete_after=20)
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

        if enableWhitelistRemove:
            removeFromNameList(whitelist_file, mcName)
            await ctx.reply("Your account has been unlinked from the server and"
                            "you have been removed from the whitelist, you may"
                            "request access at another point",
                            mention_author=True)
        else:
            await ctx.reply("Your account has been unlinked from the server."
                            "Contact the server owner to be removed from the"
                            "whitelist, after which you may request access"
                            "at another point",
                            mention_author=True)
        return

    elif ctx.author.guild_permissions.manage_messages.flag:
        if isinstance(arg, Member):
            user: Member = arg
            line = removeFromUIDNameListByUserID(discordmclinklist_file, user.id)
            mcName = line.split(" ")[1]

            if enableWhitelistRemove:
                removeFromNameList(whitelist_file, mcName)
                await ctx.reply("This account has been unlinked from the server and"
                                "removed from the whitelist",
                                mention_author=True)
            else:
                await ctx.reply("This account has been unlinked from the server."
                                "Contact the server owner to remove this user from"
                                "the whitelist",
                                mention_author=True)
    else:
        await ctx.reply("You are only allowed to use this command as an"
                        "empty message", mention_author=True, delete_after=20)
        return


@bot.command()
@commands.has_permissions(manage_messages=True)
async def addtodenylist(ctx: commands.Context, arg: str):
    member: Member = MemberConverter().convert(ctx, arg)
    appendToFile(denylist_file, member.id)

    await ctx.reply("That user was barred from requesting access to the server",
                    mention_author=True, delete_after=20)
    return


@bot.command()
@commands.has_permissions(manage_messages=True)
async def removefromdenylist(ctx: commands.Context, arg: str):
    member: Member = MemberConverter().convert(ctx, arg)
    removeFromUIDList(denylist_file, member.id)

    await ctx.reply("That user is now allowed to request access to the server",
              mention_author=True, delete_after=20)
    return


@bot.command()
@commands.has_permissions(manage_messages=True)
async def overrideadd(ctx: commands.Context, name: str):
    appendToFile(whitelist_file, name)

    await ctx.reply("That user has been added to the whitelist ONLY, not to"
                    "the discord link, the only way to remove this user is to"
                    "use the banfromwhitelist command", mention_author=True,
                    delete_after=20)
    return


@bot.command()
@commands.has_permissions(manage_messages=True)
async def banFromWhitelist(ctx: commands.Context, mcname):
    if enableWhitelistRemove:
        removeFromNameList(whitelist_file, mcname)
        removeFromUIDNameListByMCName(discordmclinklist_file, mcname)
        await ctx.reply("That user has been removed from the whitelist and had"
                    "their account unlinked, if you meant to prevent whitelist"
                    "requests, use addtodenylist command", mention_author=True,
                        delete_after=30)
    else:
        await ctx.reply("This command is disabled by the server owner",
                        mention_author=True, delete_after=20)
    return


@bot.command()
@commands.has_permissions(manage_messages=True)
async def toggleSelfWhitelist(ctx: commands.Context, duration: str):
    hours = float(duration)
    super.selfWhiteList = not selfWhiteList

    if selfWhiteList:
        if super.threadTimerActive:
            super.threadTimerActive = False
        else:
            super.threadTimerActive = True
            await ctx.send("Self whitelisting has been turned on for "
                           + hours +
                           " hours or until turned off manually",
                           mention_author=True)
            asyncio.run(turnOffSelfWhitelistThreaded(hours))


async def turnOffSelfWhitelistThreaded(duration: float):
    hours = duration * 60 * 60
    await asyncio.wait_for(asyncio.Condition().wait_for(not threadTimerActive), hours)
    super.selfWhiteList = False
    return


