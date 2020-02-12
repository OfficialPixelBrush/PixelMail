from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import smtplib
import easyimap
from email.message import EmailMessage
import os.path
from os import path
from pathlib import Path
import base64
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



google_default_smtp = "smtp.gmail.com"
google_port_smtp = 465
google_default_imap = "imap.gmail.com"

pixelmail_session = Path("")

print("Reading Session File...")
if os.path.isfile("pixelmail_session"):
    session_file = open("pixelmail_session", "r")
    sender_txt = session_file.readline()
    passwd_txt = session_file.readline()
    server_smtp_txt = session_file.readline()
    server_imap_txt = session_file.readline()
    server_port_txt = session_file.readline()
    sender_txt = sender_txt.strip()
    passwd_txt = passwd_txt.strip()
    server_smtp_txt = server_smtp_txt.strip()
    server_imap_txt = server_imap_txt.strip()
    server_port_txt = server_port_txt.strip()
    sender_txt = sender_txt.replace(" ", "")
    passwd_txt = passwd_txt.replace(" ", "")
    server_smtp_txt = server_smtp_txt.replace(" ", "")
    server_imap_txt = server_imap_txt.replace(" ", "")
    server_port_txt = server_port_txt.replace(" ", "")
    session_file.close()
    print("Loaded Session File")

root = Tk()
root.title("PixelMail")
tabControl = ttk.Notebook(root)          # Create Tab Control
tab1 = ttk.Frame(tabControl)            # Create a tab 
tabControl.add(tab1, text='Sending')      # Add the tab
tabControl.pack(expand=1, fill=BOTH)  # Pack to make visible
tab2 = ttk.Frame(tabControl)            # Create a tab 
tabControl.add(tab2, text='Receiving')      # Add the tab
tabControl.pack(expand=1, fill=BOTH)  # Pack to make visible

def port587():
    print("No SLL detected")
    print("Compiling Mail...")
    msg = MIMEMultipart()
    message = mail_message.get('1.0',END)
    msg['From']=sender.get()
    msg['To']=recipient.get()
    msg['Subject']=subject.get()
    msg.attach(MIMEText(message, 'plain'))
    print("Mail Compiled")
    print("Connecting to Server...")
    server = smtplib.SMTP(host=server_smtp.get(), port=server_port.get())
    print("Greeting Server...")
    server.ehlo(server_smtp.get())
    server.starttls()
    print("Logging in...")
    server.login(sender.get(), passwd.get())
    print("Sending Mail...")
    server.send_message(msg)
    text_report_label.config(text="Mail sent")
    print("Mail sent")
    server.quit()
    print("Disconnected from Server")


def portOther():
    print("SLL detected")
    print("Compiling Mail...")
    msg = MIMEMultipart()
    message = mail_message.get('1.0',END)
    msg['From']=sender.get()
    msg['To']=recipient.get()
    msg['Subject']=subject.get()
    msg.attach(MIMEText(message, 'plain'))
    print("Mail Compiled")
    print("Connecting to Server...")
    server = smtplib.SMTP_SSL(host=server_smtp.get(), port=server_port.get())
    print("Greeting Server...")
    server.ehlo()
    print("Logging in...")
    server.login(sender.get(), passwd.get())
    print("Sending Mail...")
    server.send_message(msg)
    text_report_label.config(text="Mail sent")
    print("Mail sent")
    server.quit()
    print("Disconnected from Server")
    

def sendMail():
    if server_port.get() != "587":
        portOther()
    else:
        port587()

def setGoogle():
    server_smtp.delete(0,END)
    server_smtp.insert(0,google_default_smtp)
    server_imap.delete(0,END)
    server_imap.insert(0,google_default_imap)
    server_port.delete(0,END)
    server_port.insert(0,google_port_smtp)

def showPasswd():
    if showPassword.get() == 1:
        passwd.config(show="");
    else:
        passwd.config(show="*");

def loadMail():
    print("Loading Mail File...")   
    mail_file = open("pixelmail_mail", "r")
    recipient.delete(0,END)
    recipient.insert(0,mail_file.readline())
    subject.delete(0,END)
    subject.insert(0,mail_file.readline())  
    mail_message.delete('1.0',END)
    mail_message.insert('1.0',mail_file.read()) 
    mail_file.close() 
    temp_rep = recipient.get().strip().replace(" ", "")
    recipient.delete(0,END)
    recipient.insert(0,temp_rep)
    text_report_label.config(text="Mail loaded")
    print("Mail File Loaded")
    
def saveMail():
    print("Saving to Mail File...")
    mail_file = open("pixelmail_mail", "w")
    mail_file.write(recipient.get() + "\n")
    mail_file.write(subject.get() + "\n")
    mail_file.write(mail_message.get("1.0",END))
    mail_file.close() 
    text_report_label.config(text="Mail saved")
    print("Mail File Saved")

def saveLogin():
    print("Writing to Session File...")
    session_file = open("pixelmail_session", "w")
    session_file.write(sender.get() + "\n")
    session_file.write(passwd.get() + "\n")
    session_file.write(server_smtp.get() + "\n")
    session_file.write(server_imap.get() + "\n")
    session_file.write(server_port.get())
    session_file.close() 
    print("Written to Session File")
    text_report_label.config(text="Login Saved")

# SENDING MAIL TAB (tab1)

info = Frame()
info.pack(fill=X)

server_smtp_label = Label(info, text="Server (SMTP)")
server_smtp_label.grid(row=1,sticky=W)
server_smtp = Entry(info, width=50)
server_smtp.grid(row=1, column=1)

server_imap_label = Label(info, text="Server (IMAP)")
server_imap_label.grid(row=3,sticky=W)
server_imap = Entry(info, width=50)
server_imap.grid(row=3, column=1)

port_label = Label(info, text="Server Port")
port_label.grid(row=2, sticky=W)
server_port = Entry(info, width=50)
server_port.grid(row=2, column=1)

google_button = Button(info, text ="Gmail Default", command = setGoogle)
google_button.grid(row=2, column=3)



sender_label = Label(info, text="Sender E-Mail")
sender_label.grid(row=4, sticky=W)
sender = Entry(info, width=50)
sender.grid(row=4, column=1)

passwd_label = Label(info, text="Password")
passwd_label.grid(row=5, sticky=W)
passwd = Entry(info, show="*", width=50)
passwd.grid(row=5, column=1)

showPassword = IntVar()
show_password = Checkbutton(info, text ="Show", command = showPasswd, variable=showPassword)
show_password.grid(row=5, column=3)

save_Login = Button(info, text ="Save Login", command = saveLogin)
save_Login.grid(row=5, column=4)



recipient_lab = Label(tab1, text="Recipient")
recipient_lab.grid(row=6, sticky=W)
recipient = Entry(tab1, width=50)
recipient.grid(row=7, sticky=EW)

subject_lab = Label(tab1, text="Subject")
subject_lab.grid(row=8, sticky=W)
subject = Entry(tab1, width=50)
subject.grid(row=9, sticky=EW)



load_Mail = Button(tab1, text ="Load E-Mail", command = loadMail, width=20)
load_Mail.grid(row=10, sticky=E, pady=5, padx=5)
save_Mail = Button(tab1, text ="Save E-Mail", command = saveMail, width=20)
save_Mail.grid(row=10, sticky=W, pady=5, padx=5)

mail_message = Text(tab1)
mail_message.grid(row=14,padx=10)

send = Button(tab1, text ="Send", command = sendMail)
send.grid(row=15, sticky=EW, pady=5, padx=5)

text_sep = ttk.Separator(info, orient=HORIZONTAL)
text_sep.grid(row=13, sticky=EW, column=1, columnspan=5)
text_report_label = Label(info, text="")
text_report_label.grid(row=14, column=1, columnspan=2)



if os.path.isfile("pixelmail_session"):
    sender.delete(0,END)
    passwd.delete(0,END)
    server_smtp.delete(0,END)
    server_imap.delete(0,END)
    server_port.delete(0,END)
    sender.insert(0,sender_txt)
    passwd.insert(0,passwd_txt)
    server_smtp.insert(0,server_smtp_txt)
    server_imap.insert(0,server_imap_txt)
    server_port.insert(0,server_port_txt)


# RECEIVING MAIL TAB (tab2)    
def getMails():
    user = sender.get()
    password = passwd.get()
    imap_url = server_imap.get()
    imapper = easyimap.connect(imap_url, user, password)
    receiv_1.delete("1.0",END)
    if fullM.get() == 1:
        print("Loading Mail #{0}".format(mail_slide.get()))
        for mail_id in imapper.listids(mail_slide.get()):
            mail = imapper.mail(mail_id)
            receiv_1.delete("1.0",END)
            receiv_1.insert("1.0",mail.body + "\n")
            receiv_1.insert("1.0",mail.title + "\n")
            receiv_1.insert("1.0",mail.from_addr + "\n")
            receiv_1.insert("1.0","Mail #{0}\n".format(mail_slide.get()))
            text_report_label.config(text="Mail by " + mail.from_addr + " loaded")
            print("Mail by " + mail.from_addr + " loaded")
            
    else:
        print("Loading Mail List...")
        counter = limit_slide.get()-1
        mail_save=[]
        for mail_id in imapper.listids(limit=limit_slide.get()):
            mail_save.append(mail_id)
        for mail_id in imapper.listids(limit=limit_slide.get()):
            mail = imapper.mail(mail_save[counter])
            mailBodyShort, sep, tail = mail.body.partition('\n')
            receiv_1.insert("1.0","\n")
            receiv_1.insert("1.0","\"" + mailBodyShort + "\"\n")
            receiv_1.insert("1.0",mail.title)
            receiv_1.insert("1.0",mail.from_addr + "\n")
            receiv_1.insert("1.0","Mail #{0}\n".format(counter+1))
            counter = counter-1
            print("Mail #{0} loaded".format(counter+1))
        text_report_label.config(text="{0} Emails received".format(limit_slide.get()))
        print("Mail List Loaded")

def mail_slider():
    if fullM.get() == 1:
        mail_slide.config(state='normal')
        limit_slide.config(state=DISABLED)
    else:
        mail_slide.config(state=DISABLED)
        limit_slide.config(state='normal')
        

fullM = IntVar()
receive = Button(tab2, text ="Receive", command = getMails)
receive.grid(row=3, sticky=EW, pady=2, padx=2,column=2)
receiv_1 = Text(tab2)
receiv_1.grid(row=4,column=2, pady=2, padx=2)
mail_slide = Scale(tab2, from_=1, to=50, length=400, tickinterval=49)
mail_slide.grid(row=4,column=1)
limit_slide = Scale(tab2, from_=5, to=50, length=500, orient=HORIZONTAL, tickinterval=5)
limit_slide.grid(row=5, sticky=N,column=2)
limit_slide.set(10)
getMails()
show_contents = Checkbutton(tab2, text ="Full Mail", command=mail_slider, variable=fullM)
show_contents.grid(row=3, column=1)
text_report_label.config(text="PixelMail loaded")
print("Finished loading")

        
            
root.mainloop()
