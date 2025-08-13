from repository.database import db


class Payments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    paid = db.Column(db.Boolean, default=False)
    bank_payment_id = db.Column(db.Integer, nullable=True)
    qr_code = db.Column(db.String(100), nullable=True)
    expire_in = db.Column(db.DateTime)

    def to_dict(self):
        return {
            "id":self.id,
            "value":self.value,
            "paid":self.paid,
            "bank_payment_id":self.bank_payment_id,
            "qr_code":self.qr_code,
            "expire_in":self.expire_in
        }