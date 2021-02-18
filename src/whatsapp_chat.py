#!/usr/bin/python3

import datetime
import os
import json

def whatsapp_chat( chat_file ):
    string = open(chat_file).read()
    lines = string.split("\n")
    print( len(lines))
    messages = []
    for line in lines:
        if line[0:1] != "[":
            print( line )
            continue
        if "M] " not in line:
            print( line )
            continue
        message = {}
        parts = line.split("]")
        if ":" not in parts[1]:
            print( line )
            continue
        time_string = parts[0].replace("[", "")
        if time_string.count("/") != 2:
            print( line )
            continue

        message["time"] = datetime.datetime.strptime(time_string, "%m/%d/%y, %I:%M:%S %p")
        message["author"] = parts[1].split(":")[0]
        message["post"] = parts[1].split(":")[1]
        messages.append(message)

    print(messages_by_author(messages))

    return True
# end whatsapp_chat( chat_file ):

def messages_by_author(messages):
    print(len(messages))
    author_summary = {}
    for message in messages:
        if message["author"] in author_summary.keys():
            author_summary[message["author"]] += 1
        else:
            author_summary[message["author"]] = 1

    print(json.dumps(author_summary, indent=4))

    for author in author_summary.keys():
        print (author + "," + str(author_summary[author]))

# end messages_by_author(messages)


if __name__ == "__main__":
    return_value = whatsapp_chat( os.environ.get( "WHATSAPP_CHAT_FILE"))
    print ( "whatsapp_chat returned " + str(return_value))
