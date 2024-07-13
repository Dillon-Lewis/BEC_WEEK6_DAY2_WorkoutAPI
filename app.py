from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from connections import connection, Error

## Task 1

app = Flask(__name__)
ma = Marshmallow(app)


class CustomerSchema(ma.Schema):
    id = fields.Int(dump_only= True)
    member_name = fields.String(required= True)
    email = fields.String()

    class Meta:
        fields = ("member_name", "email")

member_schema = CustomerSchema()
members_schema = CustomerSchema(many= True)

###TASK 2

@app.route("/members", methods = ['GET'])
def get_customer_list():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)

            query = 'SELECT * FROM members;'

            cursor.execute(query)

            members = cursor.fetchall()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return members_schema.jsonify(members)
    else:
        return jsonify({"error": "Databse connection failed"}), 500


@app.route("/members", methods = ["POST"])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.message), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            new_member = (member_data["member_name"], member_data["email"])

            query = "INSERT INTO members (member_name, email) VALUES (%s, %s)"

            cursor.execute(query, new_member)
            conn.commit()

            return jsonify({'message' : 'New member has been added successfully'}), 200
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Databse connection failed"}), 500 

app.route("/members/<int:id>", methods = ["PUT"])
def update_member(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            check_query = "SELECT * FROM members WHERE id = %s"
            cursor.execute(check_query, (id,))
            customer = cursor.fetchone()
            if not customer:
                return jsonify({"error": "Customer was not found."}), 404
            
            update_member = (member_data['member name'], member_data['email'], id)

            query_update = "UPDATE members SET member_name = %s, email = %s"

            cursor.execute(query_update, update_member)
            conn.commit()
            return jsonify({'message': f"Successfully update user {id}"}), 200
        
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Databse connection failed"}), 500
    
@app.route("/members/<int:id>", methods=['DELETE'])
def delete_member(id):
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()

            check_query = "SELECT * FROM members WHERE id = %s"
            cursor.execute(check_query, (id,))
            member = cursor.fetchone()
            if not member:
                return jsonify({"error": "Member not found"})
            
            query = "DELETE FROM members WHERE id = %s"
            cursor.execute(query, (id,))
            conn.commit()

            return jsonify({"message": f"Member {id} was successfully destroyed!"})
        except Error as e:
            return jsonify(e.messages), 500
        finally:
            cursor.close()
            conn.close()
    else:
        return jsonify({"error": "Databse connection failed"}), 500
    

#### TASK 3

class MemberSchema(ma.Schema):
    id = fields.Int(dump_only= True)
    member_id = fields.Int(dump_only= True)
    focal_point = fields.String()
    length = fields.Int()

    class Meta:
        fields = ("member_id", "focal_point", "length")

workout_schema = CustomerSchema()
workouts_schema = CustomerSchema(many= True)

@app.route("/workouts", methods = ['GET'])
def get_workout_sessions():
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor(dictionary= True)

            query = 'SELECT * FROM workoutSessions;'

            cursor.execute(query)

            workouts = cursor.fetchall()
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
                return workouts_schema.jsonify(workouts)
    else:
        return jsonify({"error": "Databse connection failed"}), 500
    

@app.route("/workouts/<int:id>", methods = ["PUT"])
def find_members(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    conn = connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            check_query = "SELECT * FROM members WHERE id = %s"
            cursor.execute(check_query, (id,))
            customer = cursor.fetchone()