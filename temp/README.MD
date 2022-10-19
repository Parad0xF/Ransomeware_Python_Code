Ransomware has been one of the big lucrative businesses for cybercriminals in the past decade. I am passionate about cybersecurity, and my approach constantly involves discovering things myself. So in, one day, during one penetration testing, I decided to assemble a ransomware executable on my own. In the following article, I will show how easy to build ransomware using Python.

What Is A Ransomware
Simply put, ransomware is a piece of software that blocks a user's access to files stored on the infected machine. In real life scenarios, bad players [ cyber criminals ] manage to infect the machine by using different means [ either exploiting known / 0 day vulnerabilities or by social engineering for example ]. Once infected, the software encrypts the user's files and the hackers ask for a ransom in order to provide the user with a decryption key.

A Python Implementation Of Ransomware
Python makes is extremely easy to code any program... and a ransomware is no exception. But before talking python, I just want to make sure we all agree on the fact that this tutorial is not intended to harm anyone and that the code we are describing should not be distributed with malicious intent.

Project Dependencies
For this project to run [ in under 100 lines of code ] we are going to use the following modules [ some built into Python, some external that need to be installed with pip ]:

argparse - to accept arguments from the command line
getpass - will use the getuser() method to get the username of the victim
os - to navigate between the infected machine's directories
pathlib - to generate dynamic paths
smtplib - to send victim's information to the attacker
platform - to gather more information about the victim's machine
cryptography - will use Fernet to encrypt victim's files
dotenv - to store email credentials
MIMEMultipart and MIMEText - to compose the email sent to the attacker
Ransomware Source Code
The full source code of this project is available on GitHub. Assuming that you have created your .py file to write the project, let's dive into the code. We begin by importing all the necessary modules into the project:

Since we are going to accept terminal arguments, we should define them with the help of the argparse module:

The key attribute will be used to point to the location of the cryptographic key used to decrypt the victim's files.
The backup switch is for our own protection and will be used later on to prevent the deletion of the cryptographic key from the machine during testing.
And the directory attribute is used to point to a specific directory that we want to test on [ all files on that directory will be encrypted ].
Note that in a real life scenario, the attacker might not use arguments at all, or would only use the key attribute to accommodate the decryption of the victim's files.

We will make this a functional program, and so we will wrap each task into different functions. To begin with, let's define a function that will help us navigate between directories:


Next, we need a method to get all the files in a specific directory. However, for the attack to be as efficient as possible, we want to iterate through all possible subdirectories and encrypt as many files as we can.


So what we are doing is to define a function that takes the path of the directory as an argument. Then we specify which file extensions we are targeting [ we've named just a few in our list, but you can add as many as you want ]. Then we define file_list as an empty list that will be populated in the for loop with the paths of all files discovered in the directory and its subdirectories.

We want to be able to leverage as many data on the attack as we can. Because it is easier to send emails that to set up servers with open ports to listen to our attacks, we are going to use emails as a means to communicate between us [ the attacker ] and the malware distributed to our victim's machine:

We will use gmail for the purpose of this project, but you are free to register your email address with any provider you chose.


What this function does is to load the email_address and the password from the .env file. We format the email body using MIMEMultipart() [ for which we gather machine related information by leveraging the platform module ]. We start a smtp_server, login into gmail and send the message.

Note that, since we are using dotenv to store sensitive info [ email_address and password ] , we will also need to create a .env file. Inside it, just define the following variables and save it:


gmail_account='<YOUR_GMAIL_ADDRESS>'
gmail_password='<YOUR_GMAIL_PASSWORD>'
Any ransomware attack uses cryptography to basically prevent the victim's access to their files. For this, we will need two things: a cryptographic key and the means to encrypt the files. Here is how we are going to approach this:


Above we have defined two functions. The first one uses the Fernet module to generate a cryptographic key, which is then stored in the current directory as cryptographic_key.key. Once created this file, we call the send_email function that will communicate us information about the attack.

The second function is where the actual encryption takes place. As you can see, it takes as an argument a file_list which will later see that is the same file list returned by the get_files_in_dir function. So what we are doing is to iterate through each document in that list and use Fernet's encrypt method encrypt and rewrite the original files with the contents of the encrypted one.

If the --backup switch is turned off, then we proceed to the deletion of the cryptographic key from the victim's machine, such that the victim will have to contact us [ the attacker ] in order to receive it. Remember we've sent the key via gmail.

And since we are already discussing decryption, here is how it's done:


We take the file_list that holds the encrypted files and the cryptographic_key as arguments and we iterate through all the files, using Fernet's decrypt this time. It's quite similar to the encryption function, except it decrypts...

We are now so close to finishing our Ransomware. All we have to do is to 'glue the pieces together' and find a use for the functions we have defined. And for a grand finale, I find it quite eleganant:



Basically, the code says: if we have a key, we should navigate to the encrypted directory, get all the files in it and decrypt the; else, just encrypt them.

Conclusions
Understanding malware and ransomware in particular takes a lot more effort in reality. Without the help of Fernet for example, one would need to read entire libraries of computer cryptography in order to master such a cyber attack. Today however, with the help of Python and the community, it only takes about half an hour to create a ransomware.

P.S. If you want to become a hacker, I would suggest you play on the good side and stay out of trouble. Do not use this software for bad purposes, but instead use it to learn how to code and how to help others by hacking.