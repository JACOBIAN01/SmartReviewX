import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from ReviewX import CodingalReviewer  # Import the class
app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global reviewer instance - only one review session at a time
reviewer = None

@app.route("/")
def home():
    return render_template("index.html")

@socketio.on('start_review')
def handle_review(data):
    global reviewer
    
    number = data.get("number")
    password = data.get("password")

    # Callback function to send updates back to client
    def send_update(msg):
        if reviewer:
            socketio.emit("Project_Count_Update", reviewer.get_project_count())
            socketio.emit("User_Details", reviewer.get_user_details())
        socketio.emit("review_update", msg)
    
    def Send_Review_Tracker(msg):
        socketio.emit("review_tracker", msg)

    try:
        # Create a new reviewer instance
        reviewer = CodingalReviewer(number, password, log_callback=send_update,review_callback=Send_Review_Tracker)
        
        # Run the review process in background
        socketio.start_background_task(reviewer.start_review)
    except Exception as e:
        socketio.emit("review_update", f"❌ Error occurred: {str(e)}")


@socketio.on("Cancel_Review")
def handle_cancel():
    global reviewer
    if reviewer:
        reviewer.cancel()
        socketio.emit("review_update", "⚠️ Review process was cancelled.")
    else:
        socketio.emit("review_update", "⚠️ No active review to cancel.")

if __name__ == '__main__':
    print("http://127.0.0.1:5000/")
    socketio.run(app, host='127.0.0.1', port=5000, debug=False)
