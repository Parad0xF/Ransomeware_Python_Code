The past decade has seen ransomware emerge as a highly profitable endeavor for cybercriminals. As an individual with a strong interest in cybersecurity, I have taken an active approach to learning by experimenting and discovering new information on my own. One such instance occurred during a penetration testing session, where I decided to develop my own ransomware executable using Python. In this article, I will demonstrate how straightforward it is to create a ransomware program utilizing Python programming language.

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



