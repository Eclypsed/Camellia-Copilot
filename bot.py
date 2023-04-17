import os
import json
import discord
from discord import app_commands
from dotenv import load_dotenv
from colorthief import ColorThief

song_dict = {}

class CamelliaDB:
    def __init__(self, name, url, altNames, artists, songType, touhouOrigin, originalSong, duration, albums, gameAppearances, links, imgs, description, variations):
        self.name = name
        self.url = url
        self.altNames = altNames
        self.links = links
        self.imgs = imgs
        song_dict[f"{name}"] = self

for file in os.listdir('CamelliaDB'):
    json_file = open(f'CamelliaDB/{file}', encoding='UTF-8')
    data = json.load(json_file)
    CamelliaDB(**data)
    json_file.close()

intents = discord.Intents.default()
intents.message_content = True
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER_ID = os.getenv('SERVER_ID')

class aclinet(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild= discord.Object(id=SERVER_ID))
            self.synced = True
        print(f"Logged in as {self.user}")

client = aclinet()
tree = app_commands.CommandTree(client)

@tree.command(name="cc-song", description="testing", guild=discord.Object(id=SERVER_ID))
async def cc_song(interaction: discord.Interaction, song: str, key: str = None):
    try:
        dbObject = song_dict[f'{song}']
        if key:
            valid_keys = ['-name', '-url', '-altNames', '-artists', '-songType', '-touhouOrigin', '-originalSong', '-duration', '-albums',
                        '-gameAppearances', '-links', '-imgs', '-description', '-variations']
            if key in valid_keys:
                if key == '-links':
                    link_data = dbObject.links
                    preview_img = dbObject.imgs[0]['filename']

                    ct = ColorThief(f"images/{preview_img}")
                    dominant_color = ct.get_color(quality=1)
                    dominant_color_hex = f"#{dominant_color[0]:02x}{dominant_color[1]:02x}{dominant_color[2]:02x}"

                    embed = discord.Embed(title=f"{song} Links", color=discord.Color.from_str(dominant_color_hex))
                    embed.set_thumbnail(url='attachment://filename.jpg')
                    thumbnail = discord.File(f"images/{preview_img}", "filename.jpg")
                    for link in link_data:
                        link_name = link['linkSource'] if link['unofficial'] is False else link['linkSource'] + " [U]"
                        embed.add_field(name=link_name, value=f"[{link['displayName']}]({link['link']})", inline=True)
                    await interaction.response.send_message(file=thumbnail, embed=embed)
                else:
                    await interaction.response.send_message(f"{getattr(dbObject, key[1:len(key) + 1])}")
        else:
            await interaction.response.send_message(f"{song} is in the database")
    except KeyError:
        await interaction.response.send_message(f"{song} is not a valid song name", ephemeral=True)

client.run(TOKEN)