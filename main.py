from flask import Flask,jsonify,flash,request
import pymysql
import mysql.connector as connection
import csv

app = Flask(__name__)

mydb = connection.connect(host="localhost", user="root", passwd="Datascientist@1949",use_pure=True,database="sys")
print(mydb.is_connected())
cursor = mydb.cursor()


@app.route("/bulk_insert" , methods=['GET','POST'])
def binserting():
		id = request.json['id']
		name = request.json['name']
		email = request.json['email']
		phone = request.json['phone']
		address = request.json['address']

		if id and name and email and phone and address=="POST":

			data = csv.reader(open("C:/Users/Ravi/Downloads/newrestful.csv"))
			next(data)
			for i in data:
				cursor.execute("INSERT INTO Stablee (id,name,email,phone,address) values(%s,%s,%s,%s,%s)", i)
				mydb.commit()
			r = 'bulk inserter'
			return jsonify(r)


@app.route("/insert" , methods=['GET','POST'])
def insertion():
	try:
		jsong = request.json
		id = jsong['id']
		name = jsong['name']
		email = jsong['email']
		phone = jsong['phone']
		address = jsong['address']

		if id and name and email and phone and address and request.method == "POST":
			query = "INSERT INTO Stablee(id,name,email,phone,address) VALUES(%s,%s,%s,%s,%s)"
			bind = (id,name,email,phone,address)
			cursor.execute(query,bind)
			mydb.commit()

			res = "inserted"
			return jsonify(res)
		else:
			return "error"
	except Exception as e:
		print(e)

@app.route("/show")
def show():
	try:
		query = ("SELECT id,name,email,phone,address FROM Stablee")
		cursor.execute(query)
		showrows = cursor.fetchall()
		res = jsonify(showrows)
		mydb.commit()
		return res
	except Exception as e:
		print("error")

@app.route("/update/" ,methods=['PUT'])
def updatation():
	try:
		jsong = request.json
		id = jsong['id']
		name = jsong['name']
		email = jsong['email']
		phone = jsong['phone']
		address = jsong['address']

		if id and name and email and phone and address and request.method == "PUT":
			query = "UPDATE Stablee SET name=%s, email=%s, phone=%s, address=%s WHERE id=%s"
			bind = (name,email,phone,address,id)
			cursor.execute(query,bind)
			mydb.commit()
			respo = "updated succesfully"
			return jsonify(respo)
		else:
			return "error"
	except Exception as e:
		print(str(e))

@app.route('/delete/<int:id>',methods=['DELETE'])

def delete_data(id):
		try:
			cursor.execute("DELETE FROM Stablee WHERE id=%s",(id,))
			mydb.commit()
			output='deleted'
			return jsonify(output)
		except Exception as e:
			print(str(e))

@app.route('/show/<int:id>' )
def show_one(id):
	try:
		cursor.execute("SELECT id , name , email , phone, address, FROM Stablee WHERE id=%s",id)
		dd = cursor.fetchone()
		rr = jsonify(dd)
		rr.status_code = 200
		mydb.commit()
		return rr
	except Exception as e:
		print(e)

if __name__ == "__main__":

	app.run(port=1800)
