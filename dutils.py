import discord
import lux.zutils
# test
def message2dict(message: discord.Message):
    return {k: getattr(message, k, None) for k in message.__slots__}

def message2embed(message: discord.Message, embed_color: discord.Color = None):
    embed = discord.Embed(
        timestamp=message.created_at
    )
    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url, url=message.jump_url)

    embed.description = f"{lux.zutils.threshold_string(message.content, 1900)}\n\n[Jump to message]({message.jump_url})"
    embed.set_footer(text=f"#{message.channel.name} | Sent at {message.created_at.isoformat('@').replace('@',' at ')[:-7]}")
    if message.embeds:
        for m_embed in message.embeds:
            if m_embed.url:
                embed.set_image(url=m_embed.url)
            if m_embed.image:
                embed.set_image(url=m_embed.image.url)
            if m_embed.video:
                embed._video = m_embed._video

            break
    if message.attachments:
        for attachment in message.attachments:
            if attachment.url:
                embed.set_image(url=attachment.url)
                break
    if embed_color:
        embed.colour = embed_color
    return embed

def mention_to_id(command_list):
    new_command = []
    import re
    reg = re.compile(r"<@?[!#&]?\d*>", re.IGNORECASE)
    for item in command_list:
        match = reg.search(item)
        if match is None:
            new_command.append(item)
        else:
            idmatch = re.compile(r"\d")
            id_chars = int("".join(idmatch.findall(item)))
            new_command.append(id_chars)
    return new_command

def is_role(client, target):
    import itertools
    target_role = [role for role in itertools.chain(*[guild.roles for guild in client.guilds]) if role.id == target]
    if target_role:
        return target_role[0]
    return None

