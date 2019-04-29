import smtplib

from email.mime.text import MIMEText

fromaddr = 'pythonpython4444@gmail.com'

toaddrs = 'abcd'

SMTPServer = 'smtp.gmail.com'

port = 465 #587

login = "pythonpython4444@gmail.com"

password = "pythonpython"


dummy_var = 2;
text_to_send = "Boarding Pass Details\n\n" + "Name: "+str(dummy_var)+"\nFrom: "+str(dummy_var)+"\nTo: "+str(dummy_var)+"\nDate: "+str(dummy_var)+"\nTime: "+str(dummy_var) + "\nGate: "+str(dummy_var)+"\nBoarding Time: "+str(dummy_var)+"\n\nThankyou for booking at Ascend..\n"
                  
try:
    msg = MIMEText(text_to_send)

    #msgtxt = "http://www.google.com"+"\n\n"+"This is a test."

    #msg.set_content(msgtxt)

    msg['Subject'] = "Test message"

    msg['From'] = fromaddr

    msg['To'] = toaddrs



    server = smtplib.SMTP_SSL(SMTPServer, port) #use smtplib.SMTP() if port is 587

    #server.startssl()

    server.login(login, password)

    server.sendmail(fromaddr, toaddrs, msg.as_string())

    server.quit()
except:
    print "error occured"

