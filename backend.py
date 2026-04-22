from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        data = request.json
        
        # Extract form data
        smtp_server = data.get('smtp_server', 'smtp.example.com')
        smtp_port = int(data.get('smtp_port', 587))
        sender_email = data.get('sender_email', '')
        recipient_email = data.get('recipient_email', '')
        subject = data.get('subject', '')
        message = data.get('message', '')
        username = data.get('username', '')  # SMTP username if needed
        password = data.get('password', '')  # SMTP password if needed
        use_auth = data.get('use_auth', 'false').lower() == 'true'
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email  # This is the spoofed address
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(message, 'plain'))
        
        # Connect to SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        
        # Login if authentication is needed
        if use_auth and username and password:
            server.login(username, password)
        
        # Send email
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        
        return jsonify({"status": "success", "message": "Email sent successfully"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to send email: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
