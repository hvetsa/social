#!/usr/bin/python3

import datetime
import os
import json
import re

ommitted_names = [ 
    "Family.C.B.G",
    "Krishnaveni Vempati",
    "Mr. Srini Vempati"
]

def whatsapp_chat( chat_file ):
    string = open(chat_file).read()
    lines = string.split("\n")
    print ( "Number of lines in the file: " + str(len(lines)) )
    messages = []
    for line in lines:
        if "[" in line and "]" in line and "/" in line and "," in line:
            if line[0:1] != "[":
                line = re.sub(r'[^\x00-\x7F]','', line)
            
            message = {}
            parts = line.split("]")
            if ":" not in parts[1]:
                # print( line )
                continue
                
            time_string = parts[0].replace("[", "")
            if time_string.count("/") != 2:
                # print( line )
                continue

            message["time"] = datetime.datetime.strptime(time_string, "%m/%d/%y, %I:%M:%S %p")
            message["author"] = parts[1].split(":")[0].strip()
            message["author"] = re.sub(r'[^\x00-\x7F]','', message["author"])
            message["post"] = parts[1].split(":")[1]
            if message["author"] in ommitted_names:
                continue
            messages.append(message)

        else:
            # print("Current line is not whatsapp message")
            # print(line)
            pass

    print ( "Number of messages filtered: " + str(len(messages)) )
    return_value = messages_by_author(messages)
    return True
# end whatsapp_chat( chat_file ):

def messages_by_author(messages):
    author_summary = {}
    for message in messages:
        if message["author"] in author_summary.keys():
            author_summary[message["author"]] += 1
        else:
            author_summary[message["author"]] = 1

    # reformatting Author Summary:
    mba = [] # messages by author
    for author in author_summary.keys():
        a = {}
        a["author"] = author
        a["message_count"] = author_summary[author]
        mba.append(a)

    smba = sorted(mba, key=lambda i: i["message_count"], reverse=True)
    
    print ("Name" + "," + "Count")
    for a in smba:
        print (a["author"] + "," + str(a["message_count"]))

# end messages_by_author(messages)


if __name__ == "__main__":
    return_value = whatsapp_chat( os.environ.get( "WHATSAPP_CHAT_FILE"))

