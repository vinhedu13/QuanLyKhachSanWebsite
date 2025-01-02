import base64
import json
import os
import smtplib
import time
import uuid
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re
import paypalrestsdk
import requests
import hmac
import hashlib
from sqlalchemy.orm import joinedload
from flask import jsonify, request, url_for, redirect, render_template, render_template_string, session
from flask_login import current_user
from idna.idnadata import scripts
from sqlalchemy import and_, or_, false
from qlkswebsite import db, models, app
from qlkswebsite.models import LoaiPhong, PhieuDatPhong
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def taoID():
    unique_id = int(time.time() * 1000) % 10 ** 9
    unique_id = int(unique_id)
    return unique_id


def ThanhToanMomo(idPhieu, tongTien):
    # Thông tin thanh toán
    endpoint = "https://test-payment.momo.vn/v2/gateway/api/create"
    accessKey = "F8BBA842ECF85"
    secretKey = "K951B6PE1waDMi640xX08PD3vg6EkVlz"
    orderInfo = "pay with MoMo"
    partnerCode = "MOMO"
    redirectUrl = "https://5c7d-115-76-109-63.ngrok-free.app/payment/redirect"
    ipnUrl = "https://5c7d-115-76-109-63.ngrok-free.app/callbackmomo"
    amount = str(tongTien)  # Số tiền thanh toán
    orderId = str(idPhieu)
    requestId = str(uuid.uuid4())
    extraData = ""
    partnerName = "MoMo Payment"
    requestType = "payWithMethod"
    storeId = "Test Store"
    autoCapture = True
    lang = "vi"
    loaiPhieu = session.get('loaiPhieu')
    extra_data = {
        'loaiPhieu': session.get('loaiPhieu', ''),
        'idKhachHang': session.get('idKhachHang', ''),
        'idLoaiPhong': session.get('idLoaiPhong', ''),
        'ngaynhan': session.get('ngaynhan', ''),
        'soLuong': session.get('soLuong', ''),
        'ngaytra': session.get('ngaytra', ''),
        'hoTen': session.get('hoTen', ''),
        'email': session.get('email', ''),
        'khachHang': session.get('khachHang', ''),
        'idPhieuThuePhong_TraPhong': session.get('idPhieuThuePhong', ''),
        'idPhong_TraPhong': session.get('idPhong_TraPhong', ''),
        'tongTien': session.get('tongTien', ''),
        'current_user': str(current_user.id)
    }
    extraData = base64.b64encode(json.dumps(extra_data).encode()).decode()
    # Tạo chữ ký
    rawSignature = f"accessKey={accessKey}&amount={amount}&extraData={extraData}&ipnUrl={ipnUrl}&orderId={orderId}&orderInfo={orderInfo}&partnerCode={partnerCode}&redirectUrl={redirectUrl}&requestId={requestId}&requestType={requestType}"
    h = hmac.new(bytes(secretKey, 'ascii'), bytes(rawSignature, 'ascii'), hashlib.sha256)
    signature = h.hexdigest()

    # Tạo dữ liệu JSON để gửi
    data = {
        'partnerCode': partnerCode,
        'orderId': orderId,
        'partnerName': partnerName,
        'storeId': storeId,
        'ipnUrl': ipnUrl,
        'amount': amount,
        'lang': lang,
        'requestType': requestType,
        'redirectUrl': redirectUrl,
        'autoCapture': autoCapture,
        'orderInfo': orderInfo,
        'requestId': requestId,
        'extraData': extraData,
        'signature': signature,
        'loaiPhieu': loaiPhieu
    }

    # Gửi yêu cầu đến MoMo
    response = requests.post(endpoint, json=data)

    # Kiểm tra phản hồi từ MoMo
    if response.status_code == 200:
        response_data = response.json()
        pay_url = response_data.get('payUrl')
        if pay_url:
            # Chuyển hướng người dùng đến payUrl
            return redirect(pay_url)
        else:
            return jsonify({'error': 'Pay URL not found in MoMo response'}), 400
    else:
        return jsonify({'error': 'Failed to connect to MoMo API', 'details': response.text}), 500


def callbackmomo():
    try:
        # Lấy dữ liệu từ yêu cầu
        data = request.json
        if not data:
            return jsonify({'message': 'No data received'}), 400

        # Lưu dữ liệu từ MoMo vào các biến
        partnerCode = data.get('partnerCode')
        orderId = data.get('orderId')
        requestId = data.get('requestId')
        amount = data.get('amount')
        orderInfo = data.get('orderInfo')
        orderType = data.get('orderType')
        transId = data.get('transId')
        resultCode = data.get('resultCode')
        message = data.get('message')
        payType = data.get('payType')
        extraData = data.get('extraData')
        responseTime = data.get('responseTime')

        # Kiểm tra trạng thái thanh toán
        if resultCode == 0:  # 0 là thanh toán thành công
            print("Payment successful!")
            print(f"Transaction ID: {transId}, Amount: {amount}, Order ID: {orderId}")
            # if session.get('loaiPhieu') == 'phieuThue':
            #     TaoPhieuThuePhong(id = orderId, ngayNhanPhong= session.get('ngaynhan'), ngayTraPhong= session.get('ngaytra'))
            #
        else:
            print(f"Payment failed. Result Code: {resultCode}, Message: {message}")

        # Tùy chọn: Lưu dữ liệu vào database hoặc xử lý logic khác
        # save_to_database(partnerCode, orderId, amount, transId, resultCode, message)

        # Phản hồi lại MoMo (quan trọng để MoMo biết rằng bạn đã nhận thông báo)
        return jsonify({'message': 'Callback received successfully'}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'Internal Server Error'}), 500


def paypal(idPhieu, tongTien):
    session['idPhieu'] = idPhieu
    session['tongTien'] = tongTien
    session['loaiPhieuPaypal'] = session.get('loaiPhieu')
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"
        },
        "redirect_urls": {
            "return_url": url_for('payment_success', _external=True),
            "cancel_url": url_for('payment_cancel', _external=True)
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Sample Item",
                    "sku": "item",
                    "price": str(int(tongTien / 25000)),
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": str(int(tongTien / 25000)),
                "currency": "USD"
            },
            "description": "This is a sample payment."
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                # Redirect khách hàng đến PayPal để thanh toán
                return redirect(link.href)
    else:
        return jsonify({"error": payment.error})


def KiemTraThoiGianNhanPhong_DatPhong(thoiGianNhan):
    thoiGianDat = datetime.now()
    thoiGianNhan = datetime.strptime(thoiGianNhan, '%Y-%m-%d %H:%M:%S')
    #thoiGianDat = datetime.strptime(thoiGianDat, '%Y-%m-%d %H:%M:%S')
    khoangThoiGian = thoiGianNhan - thoiGianDat
    return khoangThoiGian.days


def KiemTraPhongTrongTheoThoiGian(idLoaiPhong, thoiGianNhan, thoiGianTra):
    danh_sach_phong = db.session.query(models.Phong).filter(models.Phong.idLoaiPhong == idLoaiPhong).all()
    phong_da_duoc_thue = (
        db.session.query(models.Phong.id)
        .join(models.PhieuThuePhong_Phong, models.Phong.id == models.PhieuThuePhong_Phong.idPhong)
        .join(models.PhieuThuePhong, models.PhieuThuePhong_Phong.idPhieuThuePhong == models.PhieuThuePhong.id)
        .filter(
            or_(
                and_(models.PhieuThuePhong.ngayNhanPhong <= thoiGianTra,
                     models.PhieuThuePhong.ngayTraPhong > thoiGianNhan)
            )
        )
    ).distinct()

    danh_sach_phong_trong = [
        phong.id for phong in danh_sach_phong if phong.id not in {p.id for p in phong_da_duoc_thue}
    ]

    return danh_sach_phong_trong  # cái này là trả về id phòng trống


def DanhSachPhongTrong(idLoaiPhong, thoiGianNhan, thoiGianTra):
    idPhongTrong = KiemTraPhongTrongTheoThoiGian(idLoaiPhong, thoiGianNhan, thoiGianTra)
    phongTrong = []
    for idP in idPhongTrong:
        phong = models.Phong.query.get(idP)
        if phong:
            phongTrong.append(phong)
    return phongTrong  # cái này là trả về danh sách phòng trống


# def KiemTraPhongDangSuDung(thoiGianHienTai):
#     phong_dang_su_dung = (
#         db.session.query(models.Phong)
#         .join(models.PhieuThuePhong_Phong, models.Phong.id == models.PhieuThuePhong_Phong.idPhong)
#         .join(models.PhieuThuePhong, models.PhieuThuePhong_Phong.idPhieuThuePhong == models.PhieuThuePhong.id)
#         .filter(
#             and_(
#                 models.PhieuThuePhong.ngayNhanPhong <= thoiGianHienTai,
#                 models.PhieuThuePhong.ngayTraPhong > thoiGianHienTai
#             )
#         ).distinct()
#     )
#     return phong_dang_su_dung.all()  # Trả về danh sách phòng đang sử dụng


def GetPhongDangSuDung_ThoiGianTraPhongTuongUng(thoiGianHienTai):
    # Lấy danh sách phòng đang sử dụng và thời gian trả phòng tương ứng
    phong_dang_su_dung = (
        db.session.query(models.Phong, models.PhieuThuePhong)
        .join(models.PhieuThuePhong_Phong, models.Phong.id == models.PhieuThuePhong_Phong.idPhong)
        .join(models.PhieuThuePhong, models.PhieuThuePhong_Phong.idPhieuThuePhong == models.PhieuThuePhong.id)
        .join(models.PhieuThuePhong_Phong_KhachHang,
              models.PhieuThuePhong_Phong.id == models.PhieuThuePhong_Phong_KhachHang.idPhieuThuePhong_Phong)  # Thêm join với bảng Khách Hàng
        .filter(
            and_(
                models.PhieuThuePhong.ngayNhanPhong <= thoiGianHienTai,
                models.PhieuThuePhong.ngayTraPhong > thoiGianHienTai,
                models.PhieuThuePhong_Phong_KhachHang.trangThai == 'Đã nhận phòng'  # Thêm điều kiện trạng thái
            )
        )
        .distinct()
    )

    # Trả về danh sách phòng và ngayNhanPhong tương ứng
    return phong_dang_su_dung.all()  # Trả về danh sách phòng đang sử dụng cùng với ngayNhanPhong


def SoLuongLoaiPhongConTrong(idLoaiPhong, thoiGianNhan, thoiGianTra):
    # Lấy số lượng phòng thuộc loại phòng đó
    loaiPhong = db.session.query(models.LoaiPhong).filter(models.LoaiPhong.id == idLoaiPhong).first()
    if not loaiPhong:
        return 0  # Không có loại phòng này

    # Tổng số lượng phòng thuộc loại phòng
    tongSoPhong = loaiPhong.soLuong

    # Tính tổng số lượng phòng đã được đặt trong khoảng thời gian
    phongDaDat = (
        db.session.query(db.func.sum(models.PhieuDatPhong.soLuong))
        .filter(
            models.PhieuDatPhong.idLoaiPhong == idLoaiPhong,
            models.PhieuDatPhong.trangThai != 'Đã hủy',  # Bỏ qua các phiếu đặt đã hủy
            models.PhieuDatPhong.ngayNhanPhong <= thoiGianTra,
            models.PhieuDatPhong.ngayTraPhong > thoiGianNhan
        )
        .scalar()  # Trả về giá trị tổng
    )

    # Số lượng phòng đã được đặt là 0 nếu không có phiếu đặt nào
    phongDaDat = phongDaDat if phongDaDat else 0

    # Số lượng phòng còn trống
    phongConTrong = tongSoPhong - phongDaDat

    return max(phongConTrong, 0)  # Trả về 0 nếu số lượng phòng trống âm


def SoLuongPhongTrongTheoLoaiPhong(idLoaiPhong, thoiGianNhan, thoiGianTra):
    count = 0
    phongTrong = KiemTraPhongTrongTheoThoiGian(idLoaiPhong, thoiGianNhan, thoiGianTra)
    for phong in phongTrong:
        count = count + 1
    return count


def TaoPhieu(loaiPhieu, id):
    phieu = models.Phieu(loaiPhieu=loaiPhieu, thoiGianTao=datetime.now(), id=id)
    db.session.add(phieu)
    db.session.commit()
    return phieu


def TaoPhieuDatPhong(id, idKhachHang, idLoaiPhong, soLuong, ngayNhanPhong, ngayTraPhong):
    phieu = TaoPhieu(loaiPhieu='2', id=id)
    phieuDatPhong = models.PhieuDatPhong(id=phieu.id, idLoaiPhong=idLoaiPhong, idKhachHang=idKhachHang, soLuong=soLuong,
                                         ngayNhanPhong=ngayNhanPhong, ngayTraPhong=ngayTraPhong)
    db.session.add(phieuDatPhong)
    db.session.commit()
    return phieuDatPhong


def TaoKhachHang(khachHang):
    db.session.add(khachHang)
    db.session.commit()
    return khachHang


def TaoPhieuThuePhong_Phong(idPhieuThuePhong, idPhong):
    phieuThuePhong_Phong = models.PhieuThuePhong_Phong(idPhieuThuePhong=idPhieuThuePhong, idPhong=idPhong)
    db.session.add(phieuThuePhong_Phong)
    db.session.commit()
    return phieuThuePhong_Phong


def TaoPhieu_KhachHang(idKhachHang, idPhieu):
    phieu_KhachHang = models.Phieu_KhachHang(idPhieu=idPhieu, idKhachHang=idKhachHang)
    db.session.add(phieu_KhachHang)
    db.session.commit()
    return phieu_KhachHang


def TaoPhieuThuePhong_Phong_KhachHang(phieuThuePhong_Phong_KhachHang):
    db.session.add(phieuThuePhong_Phong_KhachHang)
    db.session.commit()
    return phieuThuePhong_Phong_KhachHang


def TaoPhieuThuePhong(id, ngayNhanPhong, ngayTraPhong, idPhieuDatPhong=None):
    phieu = TaoPhieu(loaiPhieu='1', id=id)
    phieuThuePhong = models.PhieuThuePhong(id=phieu.id, ngayNhanPhong=ngayNhanPhong, ngayTraPhong=ngayTraPhong,
                                           idPhieuDatPhong=idPhieuDatPhong)
    db.session.add(phieuThuePhong)
    db.session.commit()
    return phieuThuePhong


def TimKiem(ngayNhanPhong, ngayTraPhong, soLuong):
    ketQua = []
    listPhong = db.session.query(LoaiPhong).all()
    for p in listPhong:
        soPhongTrong_Thue = SoLuongPhongTrongTheoLoaiPhong(p.id, ngayNhanPhong, ngayTraPhong)
        soPhongTrong_Dat = SoLuongLoaiPhongConTrong(p.id, ngayNhanPhong, ngayTraPhong)
        if soPhongTrong_Thue > soPhongTrong_Dat:
            soPhongTrong = soPhongTrong_Dat
        elif soPhongTrong_Thue < soPhongTrong_Dat:
            soPhongTrong = soPhongTrong_Thue
        else:
            soPhongTrong = soPhongTrong_Dat
        ketQua.append({
            'id': p.id,
            'tenLoaiPhong': p.tenLoaiPhong,
            'donGia': p.donGia,
            'soPhongCon': int(soPhongTrong),
            'soLuongNguoiToiDa': p.luongKhachToiDa,
            'dienTich': p.dienTich
        })
    return ketQua


def GuiEmail(to_email, subject, message_html):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'lequangvinhkanghaneul@gmail.com'
    sender_password = 'vorv rxwe giey jpmq'

    # Tạo email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message_html, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")


def FormGuiMailDatPhong(customer_name, booking_code, checkin_date, checkout_date, room_type):
    message_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                }}
                .email-container {{
                    border: 1px solid #ccc;
                    padding: 20px;
                    width: 600px;
                    margin: auto;
                }}
                .email-header {{
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                .email-section {{
                    margin-bottom: 15px;
                }}
                .email-section strong {{
                    display: inline-block;
                    width: 150px;
                }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="email-header">Thông tin đặt phòng</div>
                <div class="email-section"><strong>Tên khách:</strong> {customer_name}</div>
                <div class="email-section"><strong>Mã đặt phòng:</strong> {booking_code}</div>
                <div class="email-section"><strong>Nhận phòng:</strong> {checkin_date}</div>
                <div class="email-section"><strong>Trả phòng:</strong> {checkout_date}</div>
                <div class="email-section"><strong>Hạng phòng:</strong> {room_type}</div>
            </div>
        </body>
        </html>
        """
    return message_html


def TachDanhSachKhachHang(danhSachKhachHang):
    import re
    input_string = danhSachKhachHang
    # Regex để tách tên khách hàng, CCCD, Loại khách và ID phòng
    matches = re.findall(r'([\w\s]+?)\s*\((\d+)\)\s*-\s*([\w\s]+)\s*-\s*(\d+)', input_string)
    customers = []
    for match in matches:
        name = match[0].strip()
        id_card = match[1].strip()
        customer_type = match[2].strip()
        room_id = match[3].strip()
        customers.append((name, id_card, customer_type, room_id))
    return customers


def TachChuoiBoiDauPhay(chuoi):
    result_list = [item.strip() for item in chuoi.split(",")]
    return result_list


def KiemTraThanhToan(idPhieu=None):
    if idPhieu == None:
        return False
    if idPhieu:
        phieu = models.Phieu.query.filter_by(id=idPhieu).first()
        if phieu.hoaDon.trangThai == 0 or phieu.hoaDon.id == None:
            return False
        if phieu.hoaDon.trangThai == 1 and phieu.hoaDon.id:
            return True


def TaoFilePDF(ten_khach_hang, ngay_nhan_phong, ngay_tra_phong, so_phong, tong_tien,
               file_name="hoa_don.pdf"):
    # Tạo canvas PDF
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter

    # Tiêu đề
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "HOA DON THANH TOAN")

    # Thông tin khách hàng
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"Ten khach hang: {ten_khach_hang}")

    # Thông tin đặt phòng
    c.drawString(50, height - 160, f"Ngay nhan phong: {ngay_nhan_phong}")
    c.drawString(50, height - 180, f"Ngay tra phong: {ngay_tra_phong}")
    c.drawString(50, height - 220, f"So phong: {so_phong}")

    # Tổng tiền
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, height - 320, f"Tong tien: {tong_tien} VND")

    # Lưu file PDF
    c.save()
    print(f"Hóa đơn đã được tạo thành công: {file_name}")

# def in_hoa_don_truc_tiep(file_path):
#     try:
#         # Kiểm tra xem file PDF có tồn tại hay không
#         if not os.path.exists(file_path):
#             print(f"File {file_path} không tồn tại.")
#             return
#
#         # Lấy máy in mặc định
#         printer_name = "Microsoft Print to PDF"
#         print(f"Sử dụng máy in: {printer_name}")
#
#         # Gửi lệnh in file PDF
#         win32api.ShellExecute(0, "print", file_path, f'"{printer_name}"', ".", 0)
#         print(f"Hóa đơn {file_path} đã được gửi đến máy in.")
#     except Exception as e:
#         print(f"Lỗi khi in hóa đơn: {e}")


def GetPhieuDatPhongByIDorKhachHang(thongTin):
    phieuDatPhong = None
    thongTin = thongTin.strip()
    khachHang = models.KhachHang.query.filter_by(tenKhachHang = thongTin).first()
    if khachHang:
        phieuDatPhong = models.PhieuDatPhong.query.filter_by(idKhachHang=khachHang.id)
    return phieuDatPhong

def GetIdLoaiPhongTuHoaDon_PhieuThue(id_hoadon):
    hoa_don = db.session.query(models.HoaDon).options(
        joinedload(models.HoaDon.phieu)
        .joinedload(models.Phieu.phieuThuePhong)
        .joinedload(models.PhieuThuePhong.phieuThuePhong_Phong)
        .joinedload(models.PhieuThuePhong_Phong.phong)
    ).filter_by(id=id_hoadon).first()

    if hoa_don and hoa_don.phieu and hoa_don.phieu.phieuThuePhong:
        phieu_thue_phong_phong = hoa_don.phieu.phieuThuePhong[0].phieuThuePhong_Phong
        if phieu_thue_phong_phong:
            return phieu_thue_phong_phong[0].phong.idLoaiPhong
    return None


def GetIdLoaiPhongTuHoaDon_PhieuDat(hoa_don_id):
    result = db.session.query(PhieuDatPhong.idLoaiPhong).join(
        models.HoaDon, models.HoaDon.idPhieu == PhieuDatPhong.id
    ).filter(models.HoaDon.id == hoa_don_id).first()
    return result[0] if result else None


if __name__ == '__main__':
    with app.app_context():
        GetPhieuDatPhongByIDorKhachHang(42)
        # a = '2024-12-23 15:00:00'
        # b = KiemTraPhongDangSuDung(a)
        # for bb in b:
        #     print(bb.id)
        # a = KiemTraPhongTrongTheoThoiGian(1, '2024-12-01 14:00:00', '2024-12-05 12:00:00')
        # print(a)
        app.run(debug=True)
