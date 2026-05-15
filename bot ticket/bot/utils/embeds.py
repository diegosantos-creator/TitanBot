import discord


def success_embed(message):

    return discord.Embed(
        description=f"✅ {message}",
        color=0x00ff00
    )


def error_embed(message):

    return discord.Embed(
        description=f"❌ {message}",
        color=0xff0000
    )


def warning_embed(message):

    return discord.Embed(
        description=f"⚠️ {message}",
        color=0xffcc00
    )


def info_embed(message):

    return discord.Embed(
        description=f"ℹ️ {message}",
        color=0x5865F2
    )