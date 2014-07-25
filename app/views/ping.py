from app import app, db

#Simple test to determine the status of the API
@app.route('/api/ping', methods=['GET', 'POST'])
def ping():
  return "PONG"