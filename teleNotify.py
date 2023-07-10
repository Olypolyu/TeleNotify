import argparse
import ast
import datetime
import random
import telebot

# Read properties
properties = {}
with open("./teleNotify.properties", "r") as f:
    for line in f:

        # Ignore comments and empty lines
        line = line.strip()
        if line.startswith("#") or line == "":
            continue

        # Split the line into key-value pairs
        key_value = line.split("=", 1)
        key = key_value[0].strip()
        value = key_value[1].strip()

        # Convert string to boolean if necessary
        if value.lower() == "false":
            properties[key] = False
            continue
        elif value.lower() == "true":
            properties[key] = True
            continue

        # Add the key-value pair to the dictionary
        properties[key] = value

# Register arguments
parser = argparse.ArgumentParser()
parser.add_argument("-t", help="Same as --sendText")
parser.add_argument("--sendText", help="Send arbitrary text.")

parser.add_argument("-d", action="store_true", help="Same as --sendDate")
parser.add_argument("--sendDate", action="store_true", help="Send the current date.")

parser.add_argument("-r", action="store_true", help="Same as --sendRestart")
parser.add_argument("--sendRestart", action="store_true", help="Notifies that the server is restarting.")

parser.add_argument("-s", action="store_true", help="Same as --sendShutDown")
parser.add_argument("--sendShutDown", action="store_true", help="Notifies that the server is shutting down.")

parser.add_argument("-o", action="store_true", help="Same as --sendOnline")
parser.add_argument("--sendOnline", action="store_true", help="Notifies that the server is online.")

parser.add_argument("--botToken", help="Overrides bot token")
parser.add_argument("--chatID", help="Overrides chat ID")

parser.add_argument("--sad", action="store_true")
parser.add_argument("--happy", action="store_true")

args = parser.parse_args()

# Override things as needed
if args.botToken is not None:
    properties["botToken"] = args.botToken

if args.chatID is not None:
    properties["chat_id"] = args.chatID

# Initialize bot
bot = telebot.TeleBot(properties["bot_Token"])
toSend = ""

if args.sendDate or args.d:
    toSend = toSend + f'\n Current date is {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'

if args.sendRestart or args.r:
    toSend = toSend + "\n Server is trying to restart..."

if args.sendOnline or args.o:
    toSend = toSend + "\n Server is online!"

if args.sendShutDown or args.s:
    toSend = toSend + "\n Server is shutting down..."

if args.sendText or args.t is not None:
    if args.t is None:
        args.t = args.sendText

    toSend = toSend + args.t

toSend = toSend.strip("\n")

if args.sad:
    toSend = f"{toSend} {random.choice(ast.literal_eval(properties['sad_emoticons']))}"

if args.happy:
    toSend = f"{toSend} {random.choice(ast.literal_eval(properties['happy_emoticons']))}"


# Send a little message if the user does not include an argument.
if toSend == "":
    print("Must include an argument.")
    exit()

if properties["chat_id"].strip() is None or "":
    print("Please add an chat id via --chatID or the properties file.")
    exit()

if properties["bot_Token"].strip() is None or "":
    print("Please add an chat id via --botToken or the properties file.")
    exit()

bot.send_message(chat_id=properties["chat_id"], text=toSend)
