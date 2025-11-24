from cs50 import SQL
from flask import Flask , redirect , render_template , request

app = Flask(__name__)
db = SQL("sqlite:///database.db")

@app.route("/")
def index():
    content = db.execute("SELECT first_name , last_name , role FROM admin_info WHERE id = 1")[0]
    year_targets = db.execute("SELECT * FROM year_targets")
    projects_stats = db.execute("SELECT status , COUNT(*) AS stat FROM projects GROUP BY status ORDER BY stat")
    data = {
        "projects_count" : db.execute("SELECT COUNT(*) AS n FROM projects")[0]["n"],
        "employees_count" : db.execute("SELECT COUNT(*) AS n FROM employees")[0]["n"],
    }
    for item in year_targets:
        if item["name"] == "money":
            item["width"] = db.execute("SELECT COALESCE(SUM(price) , 0) AS s FROM projects WHERE status = 'completed'")[0]["s"] * 100 // item["value"]
            if item["width"] > 100 :
                item["width"] = 100 
        elif item["name"] == "employees":
            item["width"] = int(data["employees_count"]) * 100 // item["value"]
            if item["width"] > 100 :
                item["width"] = 100 
        else :
            item["width"] = int(data["projects_count"]) * 100 // item["value"]
            if item["width"] > 100 :
                item["width"] = 100 
        
    for key , value in content.items():
        data[key] = value
    projects = db.execute("SELECT projects.name AS name, projects.finish_date AS finish_date, projects.status AS status, projects.price AS price , contacts.name AS client_name FROM projects JOIN contacts ON contacts.id = projects.client_id ORDER BY projects.id DESC LIMIT 5")
    tasks = db.execute("SELECT name , description , status FROM tasks ORDER BY id DESC LIMIT 3 ")
    return render_template("index.html" , info=data  , tasks=tasks, projects=projects , targets=year_targets, projects_stats=projects_stats)

@app.route("/profile" , methods=["GET" , "POST"])
def profile():
    data = db.execute("SELECT first_name , last_name , role , country  , email , number FROM admin_info WHERE id = 1")[0]
    year_targets = db.execute("SELECT * FROM year_targets")
    if request.method == "POST":
        data = {
            "first_name" : request.form.get("first-name") ,
            "last_name" : request.form.get("last-name") ,
            "role" : request.form.get("role") ,
            "country" : request.form.get("country") ,
            "email" : request.form.get("email") ,
            "number" : request.form.get("number") ,
        }
        for key , value in data.items():
            if value : 
                query = f"UPDATE admin_info SET {key} = ? WHERE id = 1"
                db.execute(query , (value , ))
            targets_data = {
                "money" : request.form.get("money"),
                "projects": request.form.get("projects"),
                "employees" : request.form.get("employees"),
                }
        for key , value in targets_data.items():
            if value:
                query = f"UPDATE year_targets SET value = ? WHERE name = '{key}'"
                db.execute(query , (value , ))
        return redirect("/profile")
    return render_template("profile.html" , data=data , targets=year_targets)


@app.route("/employees" ,methods=["GET" , "POST"])
def employees():
    employees = db.execute("SELECT * FROM employees")
    if request.method == "POST":
        data = {
            "id" : request.form.get("id"),
            "first_name" : request.form.get("first-name") ,
            "last_name" : request.form.get("last-name") ,
            "job" : request.form.get("job") ,
            "salary" : request.form.get("salary") ,
            "email" : request.form.get("email") ,
            "number" : request.form.get("number") 
        }
        if db.execute("SELECT * FROM employees WHERE id = ?" , data["id"]):
            for key , value in data.items():
                if value : 
                    query = f"UPDATE employees SET {key} = ? WHERE id = {data["id"]}"
                    db.execute(query , (value , ))
        else :
            db.execute("INSERT INTO employees (first_name , last_name , job , salary , email , number) VALUES (? , ? , ? ,? ,? ,?)", 
                       data["first_name"] , data["last_name"] , data["job"] , data["salary"] , data["email"] , data["number"])
        return redirect("/employees")   
    return render_template("employees.html" , data=employees)

@app.route("/delete_employee" , methods =["GET" , "POST"])
def delete_emplyee():
    if request.method == "POST":
        id =  request.form.get("id")
        if id :
            db.execute("DELETE FROM employees WHERE id = ?" , id)
        return redirect("/employees")
    else :    
        return redirect("/employees")



@app.route("/tasks" ,methods=["GET" , "POST"])
def tasks():
    tasks = db.execute("SELECT * FROM tasks")
    if request.method == "POST":
        data = {
            "id" : request.form.get("id"),
            "name" : request.form.get("task-name") ,
            "description" : request.form.get("description") ,
            "start_date" : request.form.get("start-date") ,
            "finish_date" : request.form.get("finish-date") ,
            "status" : request.form.get("status") , 
        }
        if db.execute("SELECT * FROM tasks WHERE id = ?" , data["id"]):
            for key , value in data.items():
                if value : 
                    query = f"UPDATE tasks SET {key} = ? WHERE id = {data["id"]}"
                    db.execute(query , (value , ))
        else :
            db.execute("INSERT INTO tasks (name , description , start_date , finish_date , status) VALUES (? , ? , ? ,? , ?)", data["name"] , data["description"] , data["start_date"] , data["finish_date"] , data["status"])
        return redirect("/tasks")   
    return render_template("tasks.html" , tasks=tasks)

@app.route("/delete_task" , methods =["GET" , "POST"])
def delete_task():
    if request.method == "POST":
        id =  request.form.get("id")
        if id :
            db.execute("DELETE FROM tasks WHERE id = ?" , id)    
            return redirect("/tasks")
    else :    
        return redirect("/tasks")
    


@app.route("/projects" , methods=["GET" , "POST"])
def projects():
    data = db.execute("SELECT projects.id AS id,projects.name AS name,projects.finish_date AS finish_date,projects.status AS status,projects.price AS price ,contacts.name AS client_name,contacts.number AS client_number FROM projects JOIN contacts ON contacts.id = projects.client_id;")
    clients = db.execute("SELECT name , number , id FROM contacts")
    if request.method == "POST":
        data = {
            "id" : request.form.get("id"),
            "name" : request.form.get("project-name") ,
            "price" : request.form.get("price") ,
            "finish_date" : request.form.get("finish-date") ,
            "status" : request.form.get("status") , 
            "client_id" : request.form.get("client-id")
        }
        if db.execute("SELECT * FROM projects WHERE id = ?" , data["id"]):
            for key , value in data.items():
                if value : 
                    query = f"UPDATE projects SET {key} = ? WHERE id = {data["id"]}"
                    db.execute(query , (value , ))
        else :
            db.execute("INSERT INTO projects (name , price , finish_date , status , client_id ) VALUES (? , ? ,? , ? , ?)", data["name"] , data["price"]  , data["finish_date"] , data["status"] , data["client_id"])
        return redirect("/projects")   
    return render_template("projects.html" , projects=data , clients=clients)

@app.route("/delete_project" , methods =["GET" , "POST"])
def delete_project():
    if request.method == "POST":
        id =  request.form.get("id")
        if id :
            db.execute("DELETE FROM projects WHERE id = ?" , id)    
            return redirect("/projects")
    else :    
        return redirect("/projects")




@app.route("/contacts" , methods=["GET" , "POST"])
def contacts():
    clients = db.execute("SELECT * FROM contacts")
    if request.method == "POST":
        data = {
            "id" : request.form.get("id"),
            "name" : request.form.get("contact-name") ,
            "role" : request.form.get("role") ,
            "number" : request.form.get("contact-number") ,
        }
        if db.execute("SELECT * FROM contacts WHERE id = ?" , data["id"]):
            for key , value in data.items():
                if value : 
                    query = f"UPDATE contacts SET {key} = ? WHERE id = {data["id"]}"
                    db.execute(query , (value , ))
        else :
            db.execute("INSERT INTO contacts (name , number , role ) VALUES (? , ? , ? )", data["name"] , data["number"] , data["role"] )
        return redirect("/contacts")   
    return render_template("contacts.html" , contacts=clients)


@app.route("/delete_contact" , methods =["GET" , "POST"])
def delete_contact():
    if request.method == "POST":
        id =  request.form.get("id")
        if id :
            db.execute("DELETE FROM projects WHERE client_id = ?" , id)
            db.execute("DELETE FROM contacts WHERE id = ?" , id)    
        return redirect("/contacts")
    else :    
        return redirect("/contacts")