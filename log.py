#import discord_notify as dn
import time
from datetime import datetime
import os
URL = "https://discordapp.com/api/webhooks/1062061512790909008/97h66KHoN-JBhCYc633_Du5o6lBzfsjcm3rrSHfbNrfTj2fbCvQifaDSUKMOJaBi5K9G"     

def init():
    global filename
    filename = "./results/{}.log".format(datetime.now().strftime("%d_%m_%Y_%H_%M_%S"))
    os.system("mkdir results")
    with open(filename, "w+") as _:
        pass
    
def log(message, end="\n"): 
    with open(filename, 'a') as file:
        file.write(message + end)
    
# def discord(message):
#     notifier = dn.Notifier(URL)
#     time.sleep(1)
#     notifier.send(message,print_message=False)

