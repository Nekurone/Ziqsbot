import discord
from discord.ext import commands

from Core import checks
from Core.config import logger, MOD_ROLE

## 7/12/2020
# This could all be a LOT cleaner
# but it _should_ work
class RoleProtection(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.mod_role = None # Should load upon first triggering of Role change

    async def process_role_change(self, member , before, after):

        # First, check if their first role is higher than mods (ie: admin), or the role being changes is out of their reach anyway
        # Also, if role is below mod role, assume it SHOULDN'T have these perms
        if self.mod_role < member.roles[0] or after > self.mod_role or member.id == after.guild.owner_id: ## For you Ziq <3:
            return 0 
            
        logger.CRITICAL("{0} Changing Permission for {0}. Demodding them and reverting".format(str(member), str(after)))
        await after.edit(permissions=before.permissions, reason="{0} Attempted to change permissions, I'll be demodding them".format(str(member)))
        new_roles = member.roles
        print(new_roles)
        if self.mod_role not in new_roles:
            logger.GENERAL("User doesn't appear to have the mod role...")
            return 1
        new_roles.remove(self.mod_role) ## I hate that this is the best way to do this.
        await member.edit(roles=new_roles, reason="Messing with the balance of nature.")
        return 1
        
    async def get_user_from_audits(self, before, after):
        member = None
        async for entry in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_update): # Checks last 5 Audit logs for a user updating this role.
            try:
                if entry.after.permissions == after.permissions:
                    ## We got (((our guy)))
                    ## Unless it was the bot.
                    if entry.user.id != self.client.user.id:
                        member = await after.guild.fetch_member(entry.user.id) #Member is not user.
                        return member
                    else:
                        return 1
            except AttributeError as e:
                logger.GENERAL("Role was changed, but no permissions changed")
        return None
            
        
    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        if self.mod_role == None: # Only triggers once when turned on
            self.mod_role = discord.utils.get(after.guild.roles, id=MOD_ROLE)
        member = await self.get_user_from_audits(before, after)
        if member == None:
            await after.edit(permissions=before.permissions, reason="Wee woo, {0} Was changed, but I ran into an error so I'm changing it back. Please report to Ziq".format(str(after)))
            logger.CRITICAL("Wee woo, {0} Was changed, but I ran into an error so I'm changing it back. Please report to Ziq".format(str(after)))
            return
        elif member == 1: ## It's just the bot, don't need to do anything
            # Actually ran into a big issue where the bot would sense itself, change the role and repeat forever
            return
        code = await self.process_role_change(member, before, after)
        if code:
            logger.CRITICAL("User mentioned above successfully demodded, and changes reverted")
            return
        logger.DEBUG("Role being updated, but was done by an admin")
        return 
        
def setup(client):
    client.add_cog(RoleProtection(client))
