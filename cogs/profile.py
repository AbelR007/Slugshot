# Discord Modules
import discord
from discord.ext import commands
import asyncio
# For Profile Image
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import urllib.request

from cogs.explore import data_list

"""
    profile
    team
"""

def Fibonacci(n):
    first = 20
    second = 30
    if n<= 0:
        print("Incorrect input")
    # First Fibonacci number is 0
    elif n == 1:
        return first
    # Second Fibonacci number is 1
    elif n == 2:
        return second
    else:
        return Fibonacci(n-1)+Fibonacci(n-2)

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def error_embed(self, ctx, content):
        embed = discord.Embed(title="Error", description=f"{content}", color=ctx.bot.error)
        return await ctx.send(embed=embed)

    async def types(self, ctx, type):
        if type == "fire":
            emoji = ctx.bot.fire
            color = discord.Colour.from_rgb(255, 102, 51)
        elif type == "water":
            emoji = "<:Water2:846955422224351232>"
            color = discord.Colour.from_rgb(0, 128, 255)
        elif type == "ice":
            emoji = "<:Ice2:846952072784248842>"
            color = discord.Colour.from_rgb(0, 255, 255)
        elif type == "energy":
            emoji = '<:Energy:846363402552344606>'
            color = discord.Colour.from_rgb(121, 255, 77)
        elif type == "electric":
            emoji = ctx.bot.electric
            color = ctx.bot.celectric
        elif type == "psychic":
            emoji = ctx.bot.psychic
            color = ctx.bot.cpsychic
        elif type == "earth":
            emoji = ctx.bot.earth
            color = ctx.bot.cearth
        elif type == "metal":
            emoji = ctx.bot.metal
            color = ctx.bot.cmetal
        elif type == "plant":
            emoji = ctx.bot.plant
            color = ctx.bot.cplant
        elif type == "air":
            emoji = ctx.bot.air
            color = ctx.bot.cair
        elif type == "toxic":
            emoji = ctx.bot.toxic
            color = ctx.bot.ctoxic
        elif type == "dark":
            emoji = ctx.bot.dark
            color = ctx.bot.cdark
        else:
            emoji = ctx.bot.slugshot
            color = ctx.bot.main
        return emoji, color

    async def profiledb(self, user_id):
        profile = await self.bot.pg_con.fetch("SELECT * FROM profile WHERE userid = $1", user_id)
        if not profile:
            await self.bot.pg_con.execute("INSERT INTO profile(userid, gold, crystal, gem) VALUES ($1, $2, $3, $4)",
                                          user_id, 0, 0, 0)
        profile = await self.bot.pg_con.fetch("SELECT * FROM profile WHERE userid = $1", user_id)
        return profile

    async def shopdb(self, user_id):
        shopdb = await self.bot.pg_con.fetchrow("SELECT * FROM shop WHERE userid = $1", user_id)
        if not shopdb:
            await self.bot.pg_con.execute("INSERT INTO shop(userid) VALUES ($1)",user_id)
        shopdb = await self.bot.pg_con.fetchrow("SELECT * FROM shop WHERE userid = $1", user_id)
        return shopdb

    @commands.command()
    async def profile(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        membername = str(member.name)

        authorid = int(member.id)
        author = await self.bot.pg_con.fetch("SELECT * FROM profile WHERE userid = $1", authorid)
        if not author:
            await self.bot.pg_con.execute("INSERT INTO profile(userid, gold, crystal, gem) VALUES ($1, $2, $3, $4)",
                                          authorid, 0, 0, 0)
        author = await self.bot.pg_con.fetch("SELECT * FROM profile WHERE userid = $1", authorid)
        gold = str(author[0]['gold'])
        crystal = str(author[0]['crystal'])

        img = Image.open(
            "D:\\Projects\\SlugShot\\img\\profile_structure.png"
        )
        # "E:\\ABEL\\Discord Bots\\SlugShot\\SlugShot Codes\\profile_structure.png"
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)

        pfp = pfp.resize((267, 267))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("fonts/quicksand.otf", 90)  # 55
        font2 = ImageFont.truetype("fonts/quicksand.otf", 45)  # 30

        draw.text((357, 155), membername, (0, 0, 0), font=font)
        draw.text((531, 283), gold, (0, 0, 0), font=font2)
        draw.text((531, 334), crystal, (0, 0, 0), font=font2)
        img.paste(pfp, (51, 49))

        img.save("img/profile.png")

        await ctx.send(file=discord.File("img/profile.png"))

    @commands.command()
    async def team(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        user_name = str(user.name)
        user_id = int(user.id)

        profiledb = await self.profiledb(user_id)

        img = Image.open(
            "D:\\Projects\\SlugShot\\img\\team_structure.png"
        )
        # "E:\\ABEL\\Discord Bots\\SlugShot\\SlugShot Codes\\profile_structure.png"
        # draw = None

        for slug_pos in range(1, 5):
            slug_id = None
            pos = None
            if slug_pos == 1:
                slug_id = profiledb[0]['team1']
                if slug_id == None:
                    continue
                    # return await ctx.send("Add slugs to the team, first!")
                pos = (64, 301)
            elif slug_pos == 2:
                slug_id = profiledb[0]['team2']
                if slug_id == None:
                    continue
                    # return await ctx.send("Add slugs to the team, first!")
                pos = (292, 301)
            elif slug_pos == 3:
                slug_id = profiledb[0]['team3']
                if slug_id == None:
                    continue
                    # return await ctx.send("Add slugs to the team, first!")
                pos = (524, 301)
            elif slug_pos == 4:
                slug_id = profiledb[0]['team4']
                if slug_id == None:
                    continue
                    # return await ctx.send("Add slugs to the team, first!")
                pos = (753, 301)
            else:
                pass
            allslugsdb = await self.bot.pg_con.fetch("SELECT * FROM allslugs WHERE slugid = $1", slug_id)
            slug_name = allslugsdb[0]['slugname']
            slugdatadb = await self.bot.pg_con.fetch("SELECT * FROM slugdata WHERE slugname = $1", slug_name)
            slug_imgurl = slugdatadb[0]['protoimgurl']

            urllib.request.urlretrieve(
                f"{slug_imgurl}",
                "img/slug_img.png"
            )
            pfp = Image.open("img/slug_img.png")
            pfp = pfp.resize((205, 205))
            draw = ImageDraw.Draw(img)
            img.paste(pfp, pos)

        font = ImageFont.truetype("fonts/quicksand.otf", 90)  # 55
        draw.text((80, 155), user_name, (0, 0, 0), font=font)

        img.save("img/team.png")

        await ctx.send(file=discord.File("img/team.png"))

    @team.error
    async def team_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(f"Send a valid member name.")

    @commands.command(
        aliases=['si']
    )
    async def sluginfo(self, ctx, *, no: str):
        global slugid
        user_id = int(ctx.message.author.id)

        profiledb = await self.bot.pg_con.fetch("SELECT * FROM profile WHERE userid = $1", user_id)
        if not profiledb:
            await self.bot.pg_con.execute("INSERT INTO profile(userid, gold, crystal, gem) VALUES ($1, $2, $3, $4)",
                                          user_id, 0, 0, 0)
        profiledb = await self.bot.pg_con.fetch("SELECT * FROM profile WHERE userid = $1", user_id)
        # print(no)
        if no == "1":
            slugid = profiledb[0]['team1']
        elif no == "2":
            slugid = profiledb[0]['team2']
        elif no == "3":
            slugid = profiledb[0]['team3']
        elif no == "4":
            slugid = profiledb[0]['team4']
        elif no in data_list:
            # print("tru")
            flag = 0
            for i in range(1, 2):  # container
                for j in range(len(data_list)):  # inside a container
                    container_pos = str(i) + '-' + str(no)
                    containerdb = await self.bot.pg_con.fetch(
                        "SELECT * FROM allslugs WHERE container_position = $1 and userid = $2", container_pos, user_id)
                    try:
                        slugid = containerdb[0]['slugid']
                    except IndexError:
                        flag = 1
                        return await ctx.send("Invalid position")
                if flag == 1:
                    break
            # return await ctx.send(f"No slug exists in the spot {no}")
        else:
            return await ctx.send("Invalid position!")

        if slugid is None or slugid == '':
            return await ctx.send("No slug at that position.")
        allslugsdb = await self.bot.pg_con.fetch("SELECT * FROM allslugs WHERE slugid = $1", slugid)
        slug_name = allslugsdb[0]['slugname']
        level = allslugsdb[0]['level']
        rank = allslugsdb[0]['rank']
        exp = allslugsdb[0]['exp']

        # region Getting the ABILITY
        abilityno = allslugsdb[0]['abilityno']
        if abilityno == 1:
            ability = "Base Ability"
        else:
            abilitydb = await self.bot.pg_con.fetchrow(
                "SELECT * FROM ability WHERE slugname = $1 AND abilityno = $2",
                slug_name, abilityno
            )
            ability = abilitydb['ability']
        # endregion

        iv_health = allslugsdb[0]['iv_health']
        iv_attack = allslugsdb[0]['iv_attack']
        iv_defense = allslugsdb[0]['iv_defense']
        iv_speed = allslugsdb[0]['iv_speed']
        iv_accuracy = allslugsdb[0]['iv_accuracy']
        iv_retrieval = allslugsdb[0]['iv_retrieval']

        ev_health = allslugsdb[0]['ev_health']
        ev_attack = allslugsdb[0]['ev_attack']
        ev_defense = allslugsdb[0]['ev_defense']
        ev_speed = allslugsdb[0]['ev_speed']
        ev_accuracy = allslugsdb[0]['ev_accuracy']
        ev_retrieval = allslugsdb[0]['ev_retrieval']

        item = allslugsdb[0]['item']
        if item == '' or item is None:
            item = "None"
        else:
            item = item.replace("_"," ").capitalize()

        slinger = self.bot.get_user(allslugsdb[0]['userid'])
        original_slinger = slinger

        slugdata = await self.bot.pg_con.fetch("SELECT * FROM slugdata WHERE slugname = $1", slug_name)

        type = slugdata[0]['type']

        health = slugdata[0]['health']
        attack = slugdata[0]['attack']
        defense = slugdata[0]['defense']
        speed = slugdata[0]['speed']
        accuracy = slugdata[0]['accuracy']
        retrieval = slugdata[0]['retrieval']

        imgurl = slugdata[0]['protoimgurl']

        type_emoji, embed_color = await self.types(ctx, type)

        embed = discord.Embed(
            color=embed_color
        )
        embed.add_field(name="Slinger", value=f"{original_slinger}")
        embed.add_field(name="Level", value=f"{level}", inline=True)
        embed.add_field(name="Experience", value=f"Rank {rank} [{exp}]", inline=True)
        # embed.add_field(name = "Type",value=type,inline=True)
        # embed.add_field(
        #     name = "Battle Stats :",
        #     value = "\u200b",
        #     inline = False
        # )
        embed.add_field(
            name="Base",
            value=f"""
            **Health**: {health}
            **Attack**: {attack}
            **Defense**: {defense}
            **Speed**: {speed}
            **Accuracy**: {accuracy}
            **Retrieval**: {retrieval}
            """,
            inline=True
        )
        embed.add_field(
            name="IVs",
            value=f"""
            **Health**: {iv_health}
            **Attack**: {iv_attack}
            **Defense**: {iv_defense}
            **Speed**: {iv_speed}
            **Accuracy**: {iv_accuracy}
            **Retrieval**: {iv_retrieval}
            """,
            inline=True
        )
        embed.add_field(
            name = "EVs",
            value = f"""
            **Health**: {ev_health}
            **Attack**: {ev_attack}
            **Defense**: {ev_defense}
            **Speed**: {ev_speed}
            **Accuracy**: {ev_accuracy}
            **Retrieval**: {ev_retrieval}
            """,
            inline = True
        )
        embed.add_field(
            name = "Item",
            value = f"{item}",
            inline = True
        )
        embed.add_field(
            name="Ability",
            value=f"{ability}",
            inline = True
        )
        embed.set_thumbnail(url=f"{imgurl}")
        embed.set_author(name=f"{slinger}", icon_url=f"{slinger.avatar_url}")
        # embed.set_footer(text = )
        await ctx.send(embed=embed)

    async def check_slugid(self, user_id, profiledb, pos):
        slug_id = 0
        if pos == "1":
            slug_id = 0  # profiledb[0]['team1']
        elif pos == "2":
            slug_id = 0  # profiledb[0]['team2']
        elif pos == "3":
            slug_id = 0  # profiledb[0]['team3']
        elif pos == "4":
            slug_id = 0  # profiledb[0]['team4']
        elif pos in data_list:
            flag = 0
            for i in range(1, 2):  # container
                for j in range(len(data_list)):  # inside a container
                    container_pos = str(i) + '-' + str(pos)
                    container_db = await self.bot.pg_con.fetch(
                        "SELECT * FROM allslugs WHERE container_position = $1 and userid = $2", container_pos, user_id)
                    try:
                        slug_id = container_db[0]['slugid']
                    except IndexError:
                        slug_id = 0
                        flag = 1
                if flag == 1:
                    break
        else:
            slug_id = 0
        return slug_id

    async def update_slugid(self, user_id, first, first_slugid, second_slugid):
        if (first != "1") or (first != "2") or (first != "3") or (first != "4"):
            first = "1-" + first
            await self.bot.pg_con.execute(
                "UPDATE allslugs SET container_position = $1 WHERE userid = $2 and slugid = $3", first, user_id,
                second_slugid
            )
        else:
            await self.bot.pg_con.execute(
                "UPDATE allslugs SET container_position = NULL WHERE userid = $1 and slugid = $2", user_id,
                second_slugid
            )
            if first == "1":
                teampos = "team1"
                await self.bot.pg_con.execute(
                    "UPDATE profile SET team1 = $1 WHERE userid = $2", first_slugid, user_id
                )
            elif first == "2":
                await self.bot.pg_con.execute(
                    "UPDATE profile SET team2 = $1 WHERE userid = $2", first_slugid, user_id
                )
            elif first == "3":
                await self.bot.pg_con.execute(
                    "UPDATE profile SET team3 = $1 WHERE userid = $2", first_slugid, user_id
                )
            else:
                await self.bot.pg_con.execute(
                    "UPDATE profile SET team4 = $1 WHERE userid = $2", first_slugid, user_id
                )

    @commands.command()
    async def upgrade(self, ctx, team_pos: int):
        user_id = ctx.message.author.id
        profiledb = await self.profiledb(user_id)

        if (team_pos == 1) or (team_pos == 2) or (team_pos == 3) or (team_pos == 4):
            pass
        else:
            return await self.error_embed(ctx, "Invalid team position number.")

        slug_id = profiledb[0][f'team{team_pos}']
        if slug_id is None or slug_id == '':
            return await self.error_embed(ctx, "No slug in that position.")

        slugdb = await self.bot.pg_con.fetchrow("SELECT * FROM allslugs WHERE slugid = $1",slug_id)
        slug_name = slugdb['slugname']
        level = slugdb['level']
        if level == 10:
            return await self.error_embed(ctx, "Slug is already at its Max Level!")

        shopdb = await self.shopdb(user_id)
        slug_type = (await self.bot.pg_con.fetchrow("SELECT * FROM slugdata WHERE slugname = $1",slug_name))['type']
        if slug_type == 'ice':
            slug_type = 'water'
        elif slug_type == 'electric' or slug_type == 'psychic':
            slug_type = 'energy'
        elif slug_type == 'metal' or slug_type == 'plant':
            slug_type = 'earth'
        elif slug_type == 'toxic':
            slug_type = 'air'
        else:
            slug_type = slug_type
        items = shopdb[f'{slug_type.lower()}_slug_food']
        items_required = Fibonacci(level)
        if items < items_required:
            return await self.error_embed(ctx, f"Insufficient number of items.\nYou require {items_required} items for the next upgrade.\nYou currently have {items} items.")

        embed = discord.Embed(
            description=f"Are you sure you want to upgrade your slug for {items_required} items?",
            color=ctx.bot.main
        )
        msg = await ctx.send(embed=embed)

        timeout_embed = discord.Embed(
            title=f"Timeout!",
            color=ctx.bot.error
        )

        tick = "\U00002611"
        cross = "\U0000274e"
        await msg.add_reaction(tick)
        await msg.add_reaction(cross)

        def check(reaction, user):
            return user == ctx.message.author and (
                    str(reaction.emoji) == tick or
                    str(reaction.emoji) == cross
            )

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            return await msg.edit(embed=timeout_embed)
        else:
            pass

        if str(reaction.emoji) == cross:
            end_embed = discord.Embed(title="Cancelled",color=ctx.bot.invis)
            return await msg.edit(embed=end_embed)

        if str(reaction.emoji) == tick:
            await self.bot.pg_con.execute(f"UPDATE allslugs SET level = $1 WHERE slugid = $2",level+1,slug_id)
            await self.bot.pg_con.execute(f"UPDATE shop SET {slug_type}_slug_food = $1 WHERE userid = $2",items - items_required,user_id)

            end_embed = discord.Embed(
                title = "Slug Levelled Up!",
                description = f"Your {slug_name.capitalize()} levelled up to Level {level + 1}",
                color = ctx.bot.success
            )
            end_embed.set_thumbnail(
                url = "https://cdn.discordapp.com/attachments/979725346658197524/980012690711904386/1653723624598.png"
            )
            return await msg.edit(embed=end_embed)

    @commands.command()
    async def boxswap(self, ctx, first, second):
        user_id = int(ctx.message.author.id)
        profiledb = await self.profiledb(user_id)

        first_slugid = await self.check_slugid(user_id, profiledb, first)
        if first_slugid == 0:
            return await ctx.send(f"No slug at position {first}")
        second_slugid = await self.check_slugid(user_id, profiledb, second)
        if second_slugid == 0:
            return await ctx.send(f"No slug at position {second}")

        first = "1-" + first
        second = "1-" + second
        await self.bot.pg_con.execute(
            "UPDATE allslugs SET container_position = $1 WHERE userid = $2 and slugid = $3", first, user_id,
            second_slugid
        )
        await self.bot.pg_con.execute(
            "UPDATE allslugs SET container_position = $1 WHERE userid = $2 and slugid = $3", second, user_id,
            first_slugid
        )
        # await self.update_slugid(user_id, first, first_slugid, second_slugid)
        # await self.update_slugid(user_id, second, second_slugid, first_slugid)
        await ctx.send("Done. Positions changed.")
        # if (second != "1") or (second != "2") or (second != "3") or (second != "4"):
        #     second = "1-" + second
        #     await self.bot.pg_con.execute("UPDATE allslugs SET container_position = $1 WHERE userid = $2 and slugid = $3",second,user_id,first_slugid)
        # else:
        #

    @commands.command()
    async def swap(self, ctx, team_pos, box_pos):
        user_id = int(ctx.message.author.id)
        profiledb = await self.profiledb(user_id)

        if team_pos == "1":
            team_slugid = profiledb[0]['team1']
        elif team_pos == "2":
            team_slugid = profiledb[0]['team2']
        elif team_pos == "3":
            team_slugid = profiledb[0]['team3']
        elif team_pos == "4":
            team_slugid = profiledb[0]['team4']
        else:
            return await ctx.send("To swap in box, use `.help boxswap`")

        box_slugid = await self.check_slugid(user_id, profiledb, box_pos)
        if box_slugid == 0:
            return await ctx.send(f"No slug at position {box_pos}")

        # print(team_slugid, box_slugid, box_slugid2)
        await self.bot.pg_con.execute(
            "UPDATE allslugs SET container_position = NULL WHERE userid = $1 AND slugid = $2",
            user_id, box_slugid
        )
        await self.bot.pg_con.execute(
            "UPDATE allslugs SET container_position = $1 WHERE userid = $2 AND slugid = $3",
            "1-"+box_pos, user_id, team_slugid
        )
        await self.bot.pg_con.execute(
            f"UPDATE profile SET team{team_pos} = $1 WHERE userid = $2",
            box_slugid, user_id
        )
        await ctx.send("Done")

    @commands.command()
    async def release(self, ctx, box_pos):
        user_id = int(ctx.message.author.id)
        profiledb = await self.profiledb(user_id)

        box_slugid = await self.check_slugid(user_id, profiledb, box_pos)
        if box_slugid == 0:
            return await ctx.send(f"No slug at position {box_pos}")

        boxdb = await self.bot.pg_con.fetch(
            "SELECT * FROM allslugs WHERE userid = $1 AND slugid = $2",
            user_id, box_slugid
        )
        slug_name = boxdb[0]['slugname']

        await self.bot.pg_con.execute(
            "UPDATE allslugs SET container_position = NULL WHERE userid = $1 AND slugid = $2",
            user_id, box_slugid
        )

        await ctx.send(f"You released a {slug_name} slug")

    @commands.command()  # IT NEEDS TO BE UPDATED
    async def bag(self, ctx, member: discord.Member = None):
        return await ctx.send("Work in progress!")
        # if member is None:
        #     member = ctx.message.author
        # # member = ctx.author if not member else member
        # # member_id = str(member.id)#Tea
        # memberid = int(member.id)
        # member = await self.bot.pg_con.fetch("SELECT * FROM profile WHERE userid = $1", memberid)
        # if not member:
        #     await self.bot.pg_con.execute("INSERT INTO profile(userid, gold, crystal, gem) VALUES ($1, $2, $3, $4)",
        #                                   memberid, 0, 0, 0)
        # member = await self.bot.pg_con.fetch("SELECT * FROM profile WHERE userid = $1", memberid)
        # gold = member[0]['gold']
        # crystal = member[0]['crystal']
        #
        # embed = discord.Embed(
        #     title=f'{member.name}\'s Bag',
        #     colour=ctx.bot.main
        # )
        # embed.set_thumbnail(
        #     url='https://media.discordapp.net/attachments/705799718478807040/743542778344112239/Untitled_design_7.png?width=427&height=427')
        # embed.add_field(name='Gold :', value=gold, inline=False)
        # embed.add_field(name='Crystals :', value=crystal, inline=False)
        # embed.set_footer(text="Requested by {}".format(ctx.message.member))
        # await ctx.send(embed=embed)

    @commands.command(
        description="Shows your wallet",
        aliases=['balance', 'bal']
    )
    async def wallet(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.message.author
        user_id = int(user.id)

        profiledb = await self.bot.pg_con.fetch("SELECT * FROM profile WHERE userid = $1", user_id)
        if not profiledb:
            await self.bot.pg_con.execute("INSERT INTO profile(userid, gold, crystal, gem) VALUES ($1, $2, $3, $4)",
                                          user_id, 0, 0, 0)
        profiledb = await self.bot.pg_con.fetch("SELECT * FROM profile WHERE userid = $1", user_id)

        gold = profiledb[0]['gold']
        crystals = profiledb[0]['crystal']
        gems = profiledb[0]['gem']

        embed = discord.Embed(
            # description =
            # f"""
            # **Gold**:
            # {gold}{ctx.bot.gold}
            #
            # **Crystals**:
            # {crystals} {ctx.bot.crystal}
            #
            # **Gems**:
            # {gems} {ctx.bot.gem}
            # """,
            color=ctx.bot.main
        )
        embed.add_field(
            name="Gold",
            value=f"{gold} {ctx.bot.gold}",
            inline=True
        )
        embed.add_field(
            name="Crystals",
            value=f"{crystals} {ctx.bot.crystal}",
            inline=True,
        )
        embed.add_field(
            name="Gems",
            value=f"{gems} {ctx.bot.gem}",
            inline=True
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/841619355958902814/976436855279058984/1652871075179.png")
        embed.set_author(name=f"{user}", icon_url=user.avatar_url)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Profile(bot))
