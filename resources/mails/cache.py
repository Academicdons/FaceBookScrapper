import smtplib
from delete import *
import urllib
import ssl
import smtplib
from email.mime.text import MIMEText

def cachedata():
    print("Starting the Cache process")
    tolist = towho()
    fro = frowho()
    paa = puss()
    
    with open("resources/whatsAppUrls.txt") as a_file:
        lines = a_file.readlines()
    
    for to in tolist:
        msg = lines
        s = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
        s.login(fro, paa)
        s.sendmail(fro, to, msg)
        
        s.close()
    print("Done Cacheing")
        


