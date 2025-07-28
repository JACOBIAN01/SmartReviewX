import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template
from flask_socketio import SocketIO, emit , join_room , leave_room
from ReviewX import CodingalReviewer  
import time


#Session_id -> reviewer instance -> Handle Multiple User
sessions = {}

app = Flask(__name__, template_folder="templates")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def home():
    return render_template("index.html")

@socketio.on('start_review')
def handle_review(data):
    session_id = data.get("session_id")
    number = data.get("number")
    password = data.get("password")

    if not session_id:
        emit("review_update","❌ Missing Session Id")
        return
    
    join_room(session_id)

    # Callback function to send updates back to client
    def send_update(msg):
        reviewer = sessions.get(session_id)
        if reviewer:
            socketio.emit("Project_Count_Update", reviewer.get_project_count(),room=session_id)
            socketio.emit("User_Details", reviewer.get_user_details(),room=session_id)
        socketio.emit("review_update", msg,room=session_id)
    
    def Send_Review_Tracker(msg):
        socketio.emit("review_tracker", msg,room=session_id)

    try:
        # Create a new reviewer instance
        reviewer = CodingalReviewer(number, password, log_callback=send_update,review_callback=Send_Review_Tracker)
        sessions[session_id] = reviewer
        # Run the review process in background
        socketio.start_background_task(reviewer.start_review)

        # Start an auto-timeout background task
        def auto_timeout():
            time.sleep(1200)
    except Exception as e:
        socketio.emit("review_update", f"❌ Error occurred: {str(e)}",room=session_id)


@socketio.on("Cancel_Review")
def handle_cancel(data):
    session_id = data.get("session_id")
    reviewer = sessions.get(session_id)
    if reviewer:
        reviewer.cancel()
        socketio.emit("review_update", "⚠️ Review process was cancelled.",room=session_id)
        leave_room(session_id)
    else:
        socketio.emit("review_update", "⚠️ No active review to cancel.",room=session_id)

if __name__ == '__main__':
    print("http://localhost:5000/")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
