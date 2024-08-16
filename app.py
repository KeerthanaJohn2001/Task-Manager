from flask import *
from functools import wraps
from flask_mysqldb import MySQL

app=Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='task_db'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)

# login
# @app.route('/')
# @app.route('/login')
# def login():
#     return render_template('login.html')


# GET ALL
@app.route('/')
@app.route('/tasks',methods=['GET'])
def tasks():
        cur=mysql.connection.cursor() 
        cur.execute("SELECT * FROM db_task")
        rows = cur.fetchall()
        cur.close()
        return render_template("tasks.html",rows=rows)
        

#ADD TASK
@app.route('/add',methods=['POST','GET'])
def add():
    status=False
    if request.method=='POST':
        Taskname=request.form["Taskname"]
        Completedat=request.form["Completedat"]
        Status=request.form["Status"]
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO db_task(Taskname,Completedat,Status) VALUES(%s,%s,%s)",(Taskname,Completedat,Status))
        mysql.connection.commit()
        cur.close()
        flash('Task added successfully.')
        return redirect(url_for('tasks'))
    return render_template("index.html",status=status)

#UPDATE
@app.route('/update/<int:taskID>', methods=['GET','POST'])
def updates(taskID):
    #fetch task
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM db_task WHERE taskID=%s",(taskID,))
    tasks=cur.fetchone()
    if request.method=='POST':
        Taskname=request.form["Taskname"]
        Completedat=request.form["Completedat"]
        Status=request.form["Status"]
        cur=mysql.connection.cursor()
        cur.execute( "UPDATE db_task set Taskname = %s, Completedat= %s,Status=%s Where taskID = %s",(Taskname,Completedat,Status,taskID))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('tasks'))
    return render_template("update.html",tasks=tasks)

# DELETE
@app.route('/delete/<int:taskID>', methods=['GET','POST'])
def delete(taskID):
    cur=mysql.connection.cursor()
    cur.execute("DELETE FROM db_task Where taskID = %s",(taskID,))
    mysql.connection.commit()
    cur.close()
    flash('Task deleted successfully.')
    return redirect(url_for('tasks'))

    



if __name__=="__main__":
    app.secret_key='secret123'
    app.run(debug=True)
    
