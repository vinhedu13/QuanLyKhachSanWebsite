import paypalrestsdk
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'your_secret_key'
# Cấu hình thông số kết nối SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:1313@localhost:3306/quanlykhachsan?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 10
db = SQLAlchemy(app)
app.secret_key = 'aiughiakjf'
login = LoginManager(app=app)
# Cấu hình PayPal
paypalrestsdk.configure({
    "mode": "sandbox",  # "sandbox" hoặc "live"
    "client_id": "AY9Se_TWXkxJ8EI_zARSrp2gqWotACp2n8mFOJOFO00ggRfAFcBUfqqI7xxueSsNyU-O1UJoXDOwItFj",  # Thay bằng Client ID
    "client_secret": "ECjyoBqJ0kVtbjj0Ybd8Cx4R4WTzdASWC5CVS1mZfsZtmYduKokbzPNCzOOMZZJGVOag8bc-fZAOK996"  # Thay bằng Secret Key
})


