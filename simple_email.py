import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_verification_email_simple(to_email, verification_code):
    """
    Изпраща email за верификация с код
    """
    try:
        # Gmail SMTP настройки
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Email credentials от environment variables
        from_email = os.getenv('EMAIL_USER', 'bulgariposveta@gmail.com')
        from_password = os.getenv('EMAIL_PASS')
        
        if not from_password:
            print("Email password not configured")
            return False
        
        # Създаване на съобщението
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = "🌹 Потвърждение на регистрация - Българи по Света"
        
        # HTML съдържание на email-а
        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; background: linear-gradient(135deg, #f7fafc, #edf2f7); padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #dc267f; margin: 0; font-size: 28px;">🌹 Българи по Света</h1>
                    <p style="color: #4a5568; margin: 10px 0 0 0;">Общност на българите по света</p>
                </div>
                
                <div style="background: linear-gradient(135deg, #dc267f, #38b2ac); padding: 3px; border-radius: 12px; margin: 20px 0;">
                    <div style="background: white; padding: 25px; border-radius: 10px; text-align: center;">
                        <h2 style="color: #2d3748; margin: 0 0 15px 0;">Добре дошли в нашата общност!</h2>
                        <p style="color: #4a5568; margin: 0 0 20px 0;">За да завършите регистрацията си, моля въведете следния код за потвърждение:</p>
                        
                        <div style="background: linear-gradient(135deg, #dc267f, #f56565); color: white; padding: 15px 30px; border-radius: 10px; font-size: 24px; font-weight: bold; letter-spacing: 3px; margin: 20px 0;">
                            {verification_code}
                        </div>
                        
                        <p style="color: #718096; font-size: 14px; margin: 20px 0 0 0;">
                            Този код е валиден за 24 часа.<br>
                            Ако не сте се регистрирали в нашия сайт, моля игнорирайте този email.
                        </p>
                    </div>
                </div>
                
                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0;">
                    <p style="color: #a0aec0; font-size: 12px; margin: 0;">
                        🌹 ❀ 🌹<br>
                        Създадено с любов за българската общност по света<br>
                        © 2024 Българи по Света
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_body, 'html', 'utf-8'))
        
        # Изпращане на email-а
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, from_password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        
        print(f"Verification email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
