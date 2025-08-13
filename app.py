from flask import Flask, request, jsonify,send_file
from repository.database import db
from db_models.payment import Payments
from payments.pix import Pix
from datetime import datetime, timedelta


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "WEBSOCKETS"
db.init_app(app)

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
    
@app.route("/payments/pix/<element>", methods=["GET"])
def get_pix(element):
    return send_file(f"static/image/{element}.png", mimetype="image/png")

@app.route("/payments/pix/confirmation",methods=["GET"])
def payments_confirmation():
    return "Confirmado"

@app.route("/payments/pix/<int:id>",methods=["GET"])
def payments_show(id):
    return "pix"

if __name__ == "__main__":
    app.run(debug=True)