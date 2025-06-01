import eventlet
eventlet.monkey_patch()
from flask import Flask ,render_template
from Review_Automation import  Start_Project_Review ,Cancel ,GetUserDetails
from flask_socketio import SocketIO,emit


app = Flask(__name__,template_folder="templates")
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def home():
    return render_template("index.html")
 
@socketio.on("Cancel_Review")
def Handle_Cancel():
    Cancel()
    socketio.emit("review_update", "⚠️ Review process was cancelled.")


@socketio.on("UserDetailsSocket")
def Handle_User_Details():
    Data = GetUserDetails()
    socketio.emit("User_Details",Data)


@socketio.on('start_review')
def handle_review(data):

    number = data.get("number")
    password = data.get("password")

    def send_update(msg):
        socketio.emit("review_update",msg)

    try:
        socketio.start_background_task(Start_Project_Review,number,password, log_callback=send_update)
    except Exception as e:
        socketio.emit("review_update", f"❌ Error occurred: {str(e)}")

if __name__ =='__main__':
    print("http://127.0.0.1:5000/")
    socketio.run(app, host='127.0.0.1', port=5000,debug=False)
