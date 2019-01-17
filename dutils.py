import discord

#test
def message2dict(message: discord.Message):
    return {k: message.__getattribute__(k) for k in message.__slots__}

def message2embed(message : discord.Message, embed_color : discord.Color = None):
    embed = discord.Embed()
    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url, url=message.jump_url)
    embed.description = message.content
    embed.set_footer(text=f"#{message.channel.name} | Sent at {message.created_at.isoformat(' at ')}")
    if message.embeds:
        for m_embed in message.embeds:
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
