from flask import Flask, render_template, request, redirect, jsonify, session, Response
import json
import os
import pandas as pd
from datetime import timedelta
from submission import Submission
from submission_digital import SubmissionDigitalTwin

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'
app.permanent_session_lifetime = timedelta(minutes=10)

submissions = {1: [], 2: [], 3: [], 4: []}
TOTAL_TASKS = 5
POINTS_PER_TASK = 20
USER_FILE = 'users.json'


def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE) as f:
            return json.load(f)
    return {}


def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)


def log_event(event_type, username):
    with open("logs.txt", "a") as f:
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} - {event_type} - {username}\n")

def log_event_CB(event_type, username, age):
    with open(f"data_{age}.txt", "a") as f:
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} - {event_type} - {username}\n")

def log_event_Digital(event_type, username):
    with open("data_digital.txt", "a") as f:
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} - {event_type} - {username}\n")
###########################Log event for delete age############################

def log_event_7_9(event_type, username):
    with open(f"delete data_7_9.txt", "a") as f:
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} - {event_type} - {username}\n")

def log_event_10_12(event_type, username):
    with open(f"delete data_10_12.txt", "a") as f:
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} - {event_type} - {username}\n")
        
def log_event_13_15(event_type, username):
    with open(f"delete data_13_15.txt", "a") as f:
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} - {event_type} - {username}\n")
        
def log_event_16_17(event_type, username):
    with open(f"delete data_16_17.txt", "a") as f:
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} - {event_type} - {username}\n")

def log_event_Digital_delete(event_type, username):
    with open("delete data_digital.txt", "a") as f:
        from datetime import datetime
        timestamp = datetime.now().isoformat()
        f.write(f"{timestamp} - {event_type} - {username}\n")        
###########################Log event for delete age############################        
        

        
#######################The End of Log event #####################################        
def load_data():
    for round_num in range(1, 5):
        filename = f"submissions_round_{round_num}.json"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                submissions[round_num] = [Submission.from_dict(entry) for entry in data]


def save_data(round_num):
    filename = f"submissions_round_{round_num}.json"
    with open(filename, 'w') as f:
        json.dump([s.to_dict() for s in submissions[round_num]], f)

#################################### Main BackEnd ########################################
@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect('/login')  # 👉 บังคับ login ก่อนเข้าหน้า index
    return render_template('index.html', username=session.get('username'))


@app.route('/submit', methods=['POST'])
def submit():
    user = request.form['user']
    checkpoint1 = int(request.form['checkpoint1'])
    checkpoint2 = int(request.form['checkpoint2'])
    deduction = int(request.form['decoration'])
    exp =  int(request.form['exp']) if request.form['exp'] and request.form['exp'].isdigit() else 0
    finish =  int(request.form['finish']) if request.form['finish'] and request.form['finish'].isdigit() else 0
    time_taken = float(request.form['time'])
    round_num = int(request.form['round'])
    age_group = request.form['age_group']
    comp_type = request.form['type']


    for submission32 in submissions[round_num]:
        if submission32.user == user and submission32.comp_type == comp_type :
            if round_num == 1:
                return Response("<script>alert('This user already exists. Duplicate entry is not allowed'); window.location.href='/';</script>",mimetype="text/html")
            elif round_num == 2:
                return Response("<script>alert('This user already exists. Duplicate entry is not allowed'); window.location.href='/dashboard_10_12';</script>",mimetype="text/html")
            elif round_num == 3:
                return Response("<script>alert('This user already exists. Duplicate entry is not allowed'); window.location.href='/dashboard_13_15';</script>",mimetype="text/html")
            elif round_num == 4:
                return Response("<script>alert('This user already exists. Duplicate entry is not allowed'); window.location.href='/dashboard_16_17';</script>",mimetype="text/html")
            
    # คำนวณคะแนนตามรุ่นอายุ
    if age_group == "7-9":
        exp = 0
        finish = 0
        score = checkpoint1 * 10 + checkpoint2 * 25 - deduction * 10
    elif age_group == "10-12":
        exp = 0
        finish = 0
        score = checkpoint1 * 10 + checkpoint2 * 25 - deduction * 5
    elif age_group == "13-15":
        score = checkpoint1 * 100 + checkpoint2 * 50 + exp + finish
    elif age_group == "16-17":
        score = checkpoint1 * 100 + checkpoint2 * 50 + exp + finish
    else:
        score = 0

    deduction = deduction * 10  # ใช้สำหรับแสดงหักคะแนน
    submission = Submission(user, checkpoint1, checkpoint2 , deduction, exp, finish, score, time_taken, age_group, comp_type)#(round, user, time_taken, score, deduction, checkpoint1, checkpoint2)
    
    submissions[round_num].append(submission)
    save_data(round_num)
    
    username=session.get('username')
    log_event_CB(f"Submit Cobot score by {username} score is =>", str(submission.to_dict()), age_group)
    #################################
    if round_num == 1:
        return redirect('/')
    elif round_num == 2:
        return redirect('/dashboard_10_12')
    elif round_num == 3:
        return redirect('/dashboard_13_15')
    elif round_num == 4:
        return redirect('/dashboard_16_17')
''' 
@app.route('/submit', methods=['POST'])
def submit():
    user = request.form['user']
    tasks = int(request.form['tasks'])
    time_taken = float(request.form['time'])
    round_num = int(request.form['round'])
    age_group = request.form['age_group']
    comp_type = request.form['type']

    score = tasks * POINTS_PER_TASK
    deductions = (TOTAL_TASKS - tasks) * POINTS_PER_TASK
    score = max(score, 0)

    submission = Submission(user, score, time_taken, deductions, age_group, comp_type)
    submissions[round_num].append(submission)
    save_data(round_num)
    return redirect('/')'''


@app.route('/rank/<int:round_num>')
def rank(round_num):
    ranked = sorted(submissions[round_num], key=lambda s: (-s.score, s.time_taken))
    return jsonify([s.to_dict() for s in ranked])


@app.route('/delete/<int:round_num>', methods=['POST'])
def delete_user(round_num):
    if not session.get('logged_in'):
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    data = request.json
    print("📥 Delete Request Received:", data)  # 🧪 print ตรงนี้

    user = data.get("user")
    time_taken = float(data.get("time_taken"))
    score = int(data.get("score"))
    age_group = data.get("age_group")
    
    print(f"🔍 Matching for: user={user}, time={time_taken}, score={score}")

    new_list = []
    deleted = False
    for s in submissions[round_num]:
        print(f"   👉 Check: {s.user=} | {s.time_taken=} | {s.score=}")
        if not deleted and s.user == user and abs(s.time_taken - time_taken) < 0.01 and s.score == score:
            print("✅ Found and deleting this one.")
            deleted = True
            continue
        new_list.append(s)
    
      
    username=session.get('username')
    if round_num == 1:
        log_event_7_9(f"Delete Cobot score by {username} score is =>", str(data))
    elif round_num == 2:
        log_event_10_12(f"Delete Cobot score by {username} score is =>", str(data))
    elif round_num == 3:
        log_event_13_15(f"Delete Cobot score by {username} score is =>", str(data))
    elif round_num == 4:
        log_event_16_17(f"Delete Cobot score by {username} score is =>", str(data))
    
    
    
    submissions[round_num] = new_list
    save_data(round_num)
    return jsonify({"success": True})


@app.route('/export')
def export():
    all_data = []
    for round_num in range(1, 5):
        for s in submissions[round_num]:
            all_data.append({
                "user": s.user,
                "checkpoint1": s.checkpoint1,
                "checkpoint2": s.checkpoint2,
                "deduction": s.deduction,
                "score": float(s.score),
                "exp" : s.exp,
                "finish" : s.finish,
                "time_taken": s.time_taken,
                "round": round_num,
                "age_group": s.age_group,
                "type": s.comp_type
            })
    df = pd.DataFrame(all_data)
    df.to_excel("submissions.xlsx", index=False)
    return jsonify({"success": True, "message": "Exported to submissions.xlsx"})

@app.route('/scores')
def scores():
    selected_round = request.args.get('round') or None
    selected_age_group = request.args.get('age_group') or None
    selected_type = request.args.get('type') or None
    all_scores = []

    for round_num in range(1, 5):
        if selected_round and str(round_num) != selected_round:
            continue
        for s in submissions[round_num]:
            if selected_age_group and s.age_group != selected_age_group:
                continue
            if selected_type and s.comp_type != selected_type:
                continue
            all_scores.append({
                "user": s.user,
                "checkpoint1": s.checkpoint1,
                "checkpoint2": s.checkpoint2,
                "deduction": s.deduction,
                "exp" : s.exp,
                "finish" : s.finish,
                "score": float(s.score),
                "time_taken": s.time_taken,
                "round": round_num,
                "age_group": s.age_group,
                "type": s.comp_type
            })

    all_scores.sort(key=lambda x: (x['round'], -x['score']))  # ✅ ใช้ key ที่ตรงกับ JSON
    return render_template('scores.html',
                           scores=all_scores,
                           logged_in=session.get('logged_in', False),
                           username=session.get('username'),
                           selected_round=selected_round,
                           selected_age_group=selected_age_group,
                           selected_type=selected_type)



@app.route('/login', methods=['GET', 'POST'])
def login():
    users = load_users()
    first_time = len(users) == 0

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if first_time:
            users[username] = password
            save_users(users)
            session.permanent = True
            session['logged_in'] = True
            session['username'] = username
            log_event("Login", username)
            return redirect('/')

        if username in users and users[username] == password:
            session.permanent = True
            session['logged_in'] = True
            session['username'] = username
            log_event("Login", username)
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid credentials", first_time=first_time)

    return render_template('login.html', first_time=first_time)


@app.route('/logout')
def logout():
    username = session.pop('username', None)
    session.pop('logged_in', None)
    if username:
        log_event("Logout", username)
    return render_template('logout.html', message=f"{username} has been logged out due to inactivity.")

# ---------------- Digital Twin ----------------

digital_submissions = []

def save_digital_data():
    with open('submissions_digital.json', 'w') as f:
        json.dump([s.to_dict() for s in digital_submissions], f)

def load_digital_data():
    global digital_submissions
    if os.path.exists('submissions_digital.json'):
        with open('submissions_digital.json') as f:
            data = json.load(f)
            digital_submissions = [SubmissionDigitalTwin.from_dict(entry) for entry in data]


@app.route('/digital_twin')
def digital_twin():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('digital_twin.html', username=session.get('username'))

@app.route('/submit_digital', methods=['POST'])
def submit_digital():
    user = request.form['user']
    cp1 = int(request.form['cp1'])
    cp2 = int(request.form['cp2'])
    finish = int(request.form['finish'])
    box_pass = int(request.form['box_pass'])
    time_taken = float(request.form['time'])

    score = (cp1 * 100) + (cp2 * 100) + (500 - (box_pass * 10)) + (finish * 100) 
    score = max(score, 0)

    submission = SubmissionDigitalTwin(user, cp1, cp2, finish, score, time_taken, box_pass)
    digital_submissions.append(submission)
    save_digital_data()
    username=session.get('username')
    log_event_Digital(f"Submit Digital score by {username} score is =>", str(submission.to_dict()))
    return redirect('/digital_twin')



@app.route('/scores_digital')
def scores_digital():
    ranked = sorted(digital_submissions, key=lambda s: (-s.score, s.time_taken))
    return render_template('scores_digital.html', scores=[s.to_dict() for s in ranked], username=session.get('username'))

@app.route('/export_digital')
def export_digital():
    all_data = []
    for s in digital_submissions:
        all_data.append({
            "User": s.user,
            "Checkpoint1": s.checkpoint1,
            "Checkpoint2": s.checkpoint2,
            "Score": float(s.score),
            "Box Passed": s.box_pass,
            "Time Taken": s.time_taken
        })
    df = pd.DataFrame(all_data)
    df.to_excel("digital_twin_submissions.xlsx", index=False)
    return jsonify({"success": True, "message": "Exported to digital_twin_submissions.xlsx"})

@app.route('/rank_digital')
def rank_digital():
    ranked = sorted(digital_submissions, key=lambda s: (-s.score, s.time_taken))
    return jsonify([s.to_dict() for s in ranked])

@app.route('/delete_digital', methods=['POST'])
def delete_digital():
    if not session.get('logged_in'):
        return jsonify({"success": False, "message": "Unauthorized"}), 403

    data = request.json
    user = data.get("user")
    time_taken = float(data.get("time_taken"))
    score = int(data.get("score"))

    global digital_submissions
    new_list = []
    deleted = False
    for s in digital_submissions:
        if not deleted and s.user == user and abs(s.time_taken - time_taken) < 0.01 and s.score == score:
            deleted = True
            continue
        new_list.append(s)
  
    digital_submissions = new_list
    save_digital_data()
    username=session.get('username')
    log_event_Digital_delete(f"delete Digital score by {username} score is =>", f"{str(data)}")
    return jsonify({"success": True})

########### New dashboard #############

@app.route('/dashboard_10_12')
def dashboard_10_12():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('dashboard_10_12.html', username=session.get('username'))

@app.route('/dashboard_13_15')
def dashboard_13_15():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('dashboard_13_15.html', username=session.get('username'))

@app.route('/dashboard_16_17')
def dashboard_16_17():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('dashboard_16_17.html', username=session.get('username'))

########### end dashboard return #############

if __name__ == '__main__':
    load_data()
    load_digital_data()
    app.run(debug=True, port=8000)
