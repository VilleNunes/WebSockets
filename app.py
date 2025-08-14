from flask import Flask, request, jsonify,send_file, render_template
from repository.database import db
from db_models.payment import Payments
from payments.pix import Pix
from datetime import datetime, timedelta
from flask_socketio import SocketIO


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "WEBSOCKETS"
db.init_app(app)
socketio = SocketIO(app)

@app.route("/payments/pix",methods=["POST"])
def create_payments():
    data = request.get_json()

    if "value" not in data:
        return jsonify({"message":"Invalid Value"}),400

    expire_in = datetime.now() + timedelta(minutes=30)
    newPayments = Payments(value=data["value"], expire_in=expire_in)

    obj_pix = Pix()
    create_pix = obj_pix.create_payments()
    newPayments.bank_payment_id = create_pix["bank_payment_id"]
    newPayments.qr_code = create_pix["qr_code"]
    db.session.add(newPayments)
    db.session.commit()

    return jsonify({
        "message":"The payment has been created",
        "payments": newPayments.to_dict()
    })
    
@app.route("/payments/qr_code/pix/<element>", methods=["GET"])
def get_pix(element):
    return send_file(f"static/image/{element}.png", mimetype="image/png")

@app.route("/payments/pix/confirmation",methods=["POST"])
def payments_confirmation():
    data = request.get_json(silent=True)

    if "bank_payment_id" not in data or "value" not in data:
        return jsonify({"message":"Invalid data"}), 400
    
    payment = Payments.query.filter_by(bank_payment_id=data.get("bank_payment_id")).first()

    if not payment or payment.paid:
        return jsonify({"message":"Payment not found"}), 404
    
    if payment.value != data.get("value"):
        return jsonify({"message":"Invalid data"}), 400
    
    payment.paid = True
    db.session.commit()
    socketio.emit(f"payment-confirmed-{payment.id}")

    return jsonify({"message":"Payments Confimation"})

@app.route("/payments/pix/<id>",methods=["GET"])
def payments_show(id):

    payments = Payments.query.get(id)

    if not payments:
        return render_template("404.html")

    if payments.paid:
        return render_template("confirmed_payment.html",value=payments.value,qr_code=payments.qr_code,payment_id=payments.id)

    return render_template("payment.html",value=payments.value,qr_code=payments.qr_code,payment_id=payments.id,host="http://127.0.0.1:5000")

@socketio.on("connect")
def connect_socket():
    print("Connect Server")
    
@socketio.on("disconnect")
def disconnect_socket():
    print("disconect server")

if __name__ == "__main__":
    socketio.run(app,debug=True)