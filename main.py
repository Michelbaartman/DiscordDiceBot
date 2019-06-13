import discord
import random
_operators = ["+", "-", "*", "/"]
_magic_answers = ["Reply hazy, try again.", "Ask again later.", "Better not tell you now.",
                  "Yes.", "Concentrate and ask again."]
_bot_commands = ["**!help** displays list of possible commands.",
                 "**!dice(dice)** rolls dice. format is (1d20+5).",
                 "**!draft** rolls 2d4-4 * 6 dice representing stats for a character"]


client = discord.Client()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!"):
        m = message.content
        u = message.author
        c = message.channel
        response = message.author.mention
        dm = False
        replace = False
        add_unf = False
        try:
            # - chat inputs - #
            if m.startswith("!dice"):
                response += chat_input_dice(m, add_unf)
                print(response)
                replace = True
            elif m.startswith("!help"):
                response = ""
                for i in _bot_commands:
                    response += i + "\n"
                dm = True
            elif m.startswith("!draft"):
                response += "🎲 Rolled **"
                for i in range(6):
                    response += str(random.randrange(1, 5) + random.randrange(1, 5) - 4) + " "
                response += "**`!draft`"
                replace = True
            else:
                response += " command doesn't exist. (try !help)"

        # error handling
        except ValueError as err:
            print("input error(Value): " + message.content)
            print(err)
            response += " " + _magic_answers[random.randrange(0, len(_magic_answers)) + "(try !help)"]

        except SyntaxError as err:
            print("input error(Syntax): " + message.content)
            print(err)
            response += " " + _magic_answers[random.randrange(0, len(_magic_answers)) + "(try !help)"]

        if dm:
            await u.send(response)
        else:
            sent = await c.send(response)
            # await sent.add_reaction(":100:")

        if replace:
            await message.delete()


def chat_input_dice(message, add_unf):
    string = ""
    dice = determine_dice(message)
    rolls = roll_dice(dice)
    total = calculate_rolls(rolls)

    if int(total) >= 20:
        add_unf = True

    string += "🎲" + " Rolled " + str(total)
    string += "  "
    for i in rolls:
        if i[0] in _operators:
            string += " " + i + " "

        elif i[0] is "(":
            temp = ""
            temp_contains_value = False
            for j in i:
                if j in _operators + ["(", ")"]:
                    if temp_contains_value:
                        string += "**" + temp + "**"
                        temp = ""
                        temp_contains_value = False
                        if j is ")":
                            string += j
                        else:
                            string += " " + j + " "
                    else:
                        string += j
                else:
                    temp += j
                    temp_contains_value = True
        else:
            string += i

    string += " `!dice("
    for i in dice:
        string += i
    string += ")`"

    return string


def determine_dice(message):
    dice_list = []
    string = message
    text_to_strip = ["!dice", "(", ")"]

    for e in text_to_strip:
        string = string.replace(e, "")
        string = "".join(string)

    dice = ""
    for i in range(len(string)):  # 1d20+5+1d4-1-1d8
        if string[i] in _operators and dice is not "":
            dice_list.append(dice.replace(" ", ""))
            dice = ""
        dice += string[i]
    dice_list.append(dice.replace(" ", ""))

    return dice_list


def roll_dice(dice_list):
    roll_list = []
    for e in dice_list:
        if e[0] in _operators:
            roll_list.append(e[0])
            e = e[1:]
        roll_list.append(e)

    for i in range(len(roll_list)):
        if "d" in roll_list[i]:
            roll = roll_list[i]
            roll_list[i] = ""
            roll = roll.split("d")
            for j in range(0, int(roll[0])):
                roll_list[i] += "+" + str(random.randrange(1, int(roll[1])+1))
            roll_list[i] = "(" + roll_list[i][1:] + ")"

    return roll_list


def calculate_rolls(roll_list):
    total = ""
    for e in roll_list:
        total += e
    try:
        total = eval(total)
    except SyntaxError:
        total = 0

    return total


client.run("client-id")
