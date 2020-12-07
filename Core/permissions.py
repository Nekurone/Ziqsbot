import asyncio
import discord

from typing import List, Iterable, Union, Dict



async def is_mod_or_superior(
    client,
    obj: Union[discord.Message, discord.Member, discord.Role]):

    if isinstance(obj, discord.Message):
        user = obj.author
    elif isinstance(obj, discord.Member):
        user = obj
    elif isinsance(obj, discord.Role):
        gid = obj.guild.id
        if obj in client.get_admin_roles(gid):
            return True
        if obj in await bot.get_mod_roles(gid):
            return True
        return False
    else:
        raise TypeError('Only Messages, Members or Roles May be Passed.')

    if await client.is_owner(user):
        return True
    if await client.is_admin(user):
        return True
    if await client.is_mod(user):
        return True
    
    return False

async def is_admin_or_superior(
    client,
    obj: Union[discord.Message, discord.Member, discord.Role]):

    if isinstance(obj, discord.Message):
        user = obj.author
    elif isinstance(obj, discord.Member):
        user = obj
    elif isinsance(obj, discord.Role):
        gid = obj.guild.id
        if obj in client.get_admin_roles(gid):
            return True
        return False
    else:
        raise TypeError('Only Messages, Members or Roles May be Passed.')

    if await client.is_owner(user):
        return True
    if await client.is_admin(user):
        return True
    
    return False



async def is_voicemod_or_superior(
    client,
    obj: Union[discord.Message, discord.Member, discord.Role]):

    if isinstance(obj, discord.Message):
        user = obj.author
    elif isinstance(obj, discord.Member):
        user = obj
    elif isinsance(obj, discord.Role):
        gid = obj.guild.id
        if obj in client.get_admin_roles(gid):
            return True
        if obj in await bot.get_mod_roles(gid):
            return True
        if obj in await bot.get_voicemod_roles(gid):
            return True
        return False
    else:
        raise TypeError('Only Messages, Members or Roles May be Passed.')

    if await client.is_owner(user):
        return True
    if await client.is_admin(user):
        return True
    if await client.is_mod(user):
        return True
    if await client.is_voicemod(user):
        return True
    
    return False
