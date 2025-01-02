import json, os
from sqlalchemy.sql import extract
from sqlalchemy.sql.functions import user
from sqlalchemy import func
from QLKSWEBSITE import db
from QLKSWEBSITE.models import TaiKhoan, KhachHang, HoaDon, PhieuDatPhong, LoaiPhong, LoaiKhach, Phong, PhieuThuePhong, \
    PhieuThuePhong_Phong
import hashlib


def add_user(username, password, **kwargs):
    if not username or not password:
        raise ValueError("Tên đăng nhập và mật khẩu không được để trống!")

    hashed_password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    khachHang = KhachHang(tenKhachHang=username.strip(), email = kwargs['email'], sdt = kwargs['phone'])
    db.session.add(khachHang)
    db.session.flush()  # Đảm bảo lấy được id của KhachHang sau khi thêm

    user = TaiKhoan(
        idKhachHang=khachHang.id,
        tenDangNhap=username,
        matKhau=password,
        soDienThoai=(kwargs.get('phone') or "").strip(),
        email=(kwargs.get('email') or "").strip()
    )

    db.session.add(user)
    db.session.commit()


# def check_login(username, password, role = None):
#     if username and password:
#         password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
#
#         return TaiKhoan.query.filter(TaiKhoan.tenDangNhap.__eq__(username.strip()),
#                                  TaiKhoan.matKhau.__eq__(password)).first()


def check_login(username, password, role=None):
    u = TaiKhoan.query.filter_by(tenDangNhap=username.strip()).first()
    if u and u.matKhau.__eq__(password):
        if role and u.idLoaiTaiKhoan.__eq__(role):
            return u
    return None


def get_user_by_id(user_id):
    return TaiKhoan.query.get(user_id)


def baocaodoanhthu_stats(kw=None, from_date=None, to_date=None):
    p = db.session.query(LoaiPhong.id, LoaiPhong.tenLoaiPhong, func.sum(LoaiPhong.donGia * PhieuDatPhong.soLuong)).join(
        PhieuDatPhong, PhieuDatPhong.idLoaiPhong.__eq__(LoaiPhong.id), isouter=True).group_by(LoaiPhong.id,
                                                                                              LoaiPhong.tenLoaiPhong)

    if kw:
        p = p.filter(LoaiPhong.tenLoaiPhong.contains(kw))
    if from_date:
        p = p.filter(PhieuDatPhong.ngayNhanPhong.__ge__(from_date))
    if to_date:
        p = p.filter(PhieuDatPhong.ngayTraPhong.__le__(to_date))
    return p.all()


def doanhthuthang_stats(year):
    return db.session.query(
        func.extract('month', HoaDon.thoiGianTao).label('month'),
        func.sum(HoaDon.tongTien).label('total_revenue')
    ).filter(
        func.extract('year', HoaDon.thoiGianTao) == year
    ).group_by(
        func.extract('month', HoaDon.thoiGianTao)
    ).order_by(
        func.extract('month', HoaDon.thoiGianTao)
    ).all()


def tuansuatsudung():
    # return db.session.query(Phong.tenPhong, func.datediff(PhieuThuePhong.ngayTraPhong, PhieuThuePhong.ngayNhanPhong).label('Số ngày thuê')).join(PhieuThuePhong_Phong,
    #                                              PhieuThuePhong_Phong.idPhong.__eq__(Phong.id)).join(PhieuThuePhong,
    #                                                                                                  PhieuThuePhong.id.__eq__(
    #                                                                                                      PhieuThuePhong_Phong.idPhieuThuePhong),
    #                                                                                                  isouter=True).group_by(
    #     Phong.tenPhong,PhieuThuePhong.ngayTraPhong, PhieuThuePhong.ngayNhanPhong).all()

    results = db.session.query(
        Phong.id.label('Phong'),
        func.sum(func.datediff(PhieuThuePhong.ngayTraPhong, PhieuThuePhong.ngayNhanPhong)).label(
            'soNgayThue'),
        func.count(PhieuThuePhong.id).label('soLanThue')
    ).join(
        PhieuThuePhong_Phong, PhieuThuePhong_Phong.idPhong == Phong.id
    ).join(
        PhieuThuePhong, PhieuThuePhong.id == PhieuThuePhong_Phong.idPhieuThuePhong
    ).group_by(
        Phong.id
    ).all()
    print(results)
    data=[]
    for result in results:
        soNgayThue = result.soNgayThue or 0
        soLanThue = result.soLanThue or 0
        tiLe = round((soNgayThue / 30) * 100, 2)  # Giả định 30 ngày trong một tháng
        data.append({
            'idPhong': result.Phong,
            'soNgayThue': soNgayThue,
            'soLanThue': soLanThue,
            'tiLe': tiLe
        })
    print(type(data))
    return data


# def tuanSuatTiLe(datas=tuansuatsudung()):
#     tiLes = []  # Danh sách chứa các tỷ lệ
#     for data in datas:
#         soNgayThue = data.soNgayThue or 0  # Nếu soNgayThue là NULL, thay thế bằng 0
#         soLanThue = data.soLanThue or 0  # Nếu soLanThue là NULL, thay thế bằng 0
#         tiLe = round((soNgayThue / 30) * 100, 2)  # Tính tỷ lệ
#         tiLes.append(tiLe)  # Thêm tỷ lệ vào danh sách
#     return tiLes  # Trả về danh sách các tỷ lệ