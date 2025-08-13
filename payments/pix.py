import uuid
import qrcode
class Pix:
    def __init__(self):
        pass

    def create_payments(self):
        bank_payment_id = str(uuid.uuid4())

        hash_payment = f"hash_payment_{bank_payment_id}"

        img = qrcode.make(hash_payment)

        img.save(f"static/image/qr_code_{hash_payment}.png")

        return {
            "bank_payment_id":bank_payment_id,
            "qr_code":f"qr_code_{hash_payment}"
        }
