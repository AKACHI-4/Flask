import smtplib 
from email.mime.text import MIMEText 

def send_mail(customer, dealer, rating, comments):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '18a0938e2a02c3'
    password = 'aacab79c718193'
    message = f"<h3>New Feedback Submission</h3> <ul><li>Customer: {customer}</li><li>Dealer: {dealer}</li><li>Rating: {rating}</li><li>Comments: {comments}</li></ul>"

    sender_email = 'abc1@example.com'
    receiver_email = 'abc2@example.com'
    # sender_email = 'IICHIPC1@gmail.com'
    # receiver_email = 'Adarshrawat8304@gmail.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'Lexus Feedback'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email 
    with smtplib.SMTP(smtp_server, port) as server: 
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())



