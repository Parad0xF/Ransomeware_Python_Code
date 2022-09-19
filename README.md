Ransomware has been one of the big lucrative businesses for cybercriminals in the past decade. I am passionate about cybersecurity, and my approach constantly involves discovering things myself. So in, one day, during one penetration testing, I decided to assemble a ransomware executable on my own. In the following article, I will show how easy to build ransomware using Python.

Project Dependencies

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



