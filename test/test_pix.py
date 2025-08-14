import sys
sys.path.append("../")
import pytest
from payments.pix import Pix
import os


def test_create_payments():
    pix_instance = Pix()
    payments_info = pix_instance.create_payments(path="../")

    assert "bank_payment_id" in payments_info 
    assert "qr_code" in payments_info

    qr_code = payments_info.get("qr_code")

    assert os.path.isfile(f"../static/image/{qr_code}.png")

