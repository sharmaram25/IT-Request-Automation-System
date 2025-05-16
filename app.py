import os
import smtplib
import uuid
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
IT_MANAGER_EMAIL = os.getenv('IT_MANAGER_EMAIL')
EXCEL_FILE = 'requests.xlsx'

# In-memory store for pending requests (replace with a database in a real application)
pending_requests = {}

def send_email(to_email, subject, body):
    try:
        msg = MIMEText(body, 'html')
        msg['Subject'] = subject
        msg['From'] = SMTP_USERNAME
        msg['To'] = to_email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

@app.route('/', methods=['GET', 'POST'])
def submit_request():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        department = request.form['department']
        request_details = request.form['request_details']

        request_id = str(uuid.uuid4())
        pending_requests[request_id] = {
            'name': name,
            'email': email,
            'department': department,
            'request_details': request_details
        }

        # Send approval email to IT Manager
        approve_url = url_for('handle_approval', request_id=request_id, decision='approved', _external=True)
        reject_url = url_for('handle_approval', request_id=request_id, decision='rejected', _external=True)
        
        email_body = render_template('approval_email.html', 
                                     name=name, email=email, department=department, 
                                     request_details=request_details, 
                                     approve_url=approve_url, reject_url=reject_url)
        
        if send_email(IT_MANAGER_EMAIL, 'New Tech Solution Request', email_body):
            # Send confirmation email to requestor
            confirmation_body = render_template('confirmation_email.html', name=name, request_details=request_details)
            send_email(email, 'Request Confirmation', confirmation_body)
            flash('Request submitted successfully! An approval email has been sent to the IT Manager.', 'success')
        else:
            flash('Failed to send approval email. Please try again later.', 'error')
            # Optionally, remove the request if email sending fails critically
            if request_id in pending_requests:
                del pending_requests[request_id]
        
        return redirect(url_for('submit_request'))
    return render_template('form.html')

@app.route('/approval/<request_id>/<decision>')
def handle_approval(request_id, decision):
    if request_id not in pending_requests:
        flash('Invalid or expired request link.', 'error')
        return redirect(url_for('submit_request'))

    request_data = pending_requests[request_id]
    status = 'approved' if decision == 'approved' else 'rejected'

    if decision == 'approved':
        # Log to Excel
        try:
            df_new = pd.DataFrame([request_data])
            if os.path.exists(EXCEL_FILE):
                df_existing = pd.read_excel(EXCEL_FILE)
                df_all = pd.concat([df_existing, df_new], ignore_index=True)
            else:
                df_all = df_new
            df_all.to_excel(EXCEL_FILE, index=False)
            flash(f'Request {request_id} has been approved and logged.', 'success')
        except Exception as e:
            flash(f'Error logging request: {e}', 'error')
            # Potentially revert status or notify admin
            status = 'approval_failed_logging' # internal status
             # Send status update to requestor
            status_update_body = render_template('status_update_email.html', 
                                            name=request_data['name'], 
                                            request_details=request_data['request_details'], 
                                            status='failed to log after approval')
            send_email(request_data['email'], 'Request Status Update', status_update_body)
            del pending_requests[request_id] # Remove from pending
            return redirect(url_for('submit_request'))


    else: # Rejected
        flash(f'Request {request_id} has been rejected.', 'success')

    # Send status update to requestor
    status_update_body = render_template('status_update_email.html', 
                                         name=request_data['name'], 
                                         request_details=request_data['request_details'], 
                                         status=status)
    send_email(request_data['email'], f'Request {status.capitalize()}', status_update_body)
    
    # Remove from pending requests
    del pending_requests[request_id]
    
    return redirect(url_for('submit_request'))

if __name__ == '__main__':
    # Create a dummy requests.xlsx if it doesn't exist, with headers
    if not os.path.exists(EXCEL_FILE):
        df_empty = pd.DataFrame(columns=['name', 'email', 'department', 'request_details'])
        df_empty.to_excel(EXCEL_FILE, index=False)
    app.run(debug=True)
