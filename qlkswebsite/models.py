import os
from ctypes.wintypes import DOUBLE
from datetime import datetime
from email.policy import default

from flask_login import UserMixin
from more_itertools.recipes import unique
from pymysql.constants.FLAG import UNSIGNED
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, column, DOUBLE, DateTime, Enum
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import relationship, backref
from qlkswebsite import db, app


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)


class TyLePhuThu(BaseModel):
    __tablename__ = 'tylephuthu'
    tyLe = db.Column(db.Double, nullable=False)


class TinhTrangPhong(BaseModel):
    __tablename__ = "tinhtrangphong"
    tenTinhTrangPhong = db.Column(db.String(50), nullable=True)
    phong = relationship('Phong', backref='tinhtrangphong', lazy = True)
    def __str__(self):
        return self.tenTinhTrangPhong


class KhachHang(BaseModel):
    __tablename__ = "khachhang"
    tenKhachHang = db.Column(db.String(50), nullable=True)
    hoKhachHang = db.Column(db.String(50), nullable=True)
    gioiTinh = db.Column(db.Enum('Nam','Nữ'), nullable=True)
    cccd = db.Column(db.String(12), nullable=True)
    sdt = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    diaChi = db.Column(db.String(200), nullable=True)
    idLoaiKhach = db.Column(db.Integer, ForeignKey('loaikhach.id'), nullable=True, info={"unsigned": True})
    phieu_khachhang = relationship('Phieu_KhachHang', backref='khachhang', lazy=True)
    phieuthuephong_phong_khachhang = relationship('PhieuThuePhong_Phong_KhachHang', backref='khachhang', lazy=True)
    taikhoan = relationship('TaiKhoan', backref='khachhang', lazy=True)
    def __str__(self):
        return (
            f"Khách hàng: {self.hoKhachHang} {self.tenKhachHang}, "
            f"Giới tính: {self.gioiTinh}, "
            f"CCCD: {self.cccd}, "
            f"Quốc tịch: {self.quocTich}, "
            f"SDT: {self.sdt}, "
            f"Email: {self.email}, "
            f"Địa chỉ: {self.diaChi}"
            f"Loại Khách: {self.idLoaiKhach}"
        )


class LoaiPhong(BaseModel):
    __tablename__ = "loaiphong"
    tenLoaiPhong = db.Column(db.String(50), nullable=False)
    donGia = db.Column(db.Double, nullable=False)
    soLuong = db.Column(db.Integer, nullable = False)
    dienTich = db.Column(db.Double, nullable = True)
    moTa = db.Column(db.String(100), nullable = True)
    luongKhachToiDa = db.Column(db.Integer, nullable = True)
    phong = relationship('Phong', backref='loaiphong', lazy=True)
    phieuDatPhong = relationship('PhieuDatPhong', backref='loaiphong', lazy=True)
    def __str__(self):
        return self.tenLoaiPhong


class Phong(BaseModel):
    __tablename__ = "phong"
    tenPhong = db.Column(db.String(50), nullable=False)
    idLoaiPhong = db.Column(db.Integer, ForeignKey('loaiphong.id'), nullable=False, info={"unsigned": True})
    idTinhTrangPhong = db.Column(db.Integer, ForeignKey('tinhtrangphong.id'), nullable=False, info={"unsigned": True})
    phieuThuePhong_Phong = relationship('PhieuThuePhong_Phong', backref='phong', lazy=True)


class LoaiPhieu(BaseModel):
    __tablename__ = "loaiphieu"
    tenLoaiPhieu = db.Column(db.String(50), nullable=False)
    phieu = relationship('Phieu', backref='loaiphieu', lazy=True)


class Phieu(BaseModel):
    __tablename__ = "phieu"
    loaiPhieu = db.Column(db.Integer, ForeignKey('loaiphieu.id'),nullable=False)
    thoiGianTao = db.Column(db.DateTime, nullable=False, default = datetime.now())
    phieuThuePhong = relationship('PhieuThuePhong', backref='phieu', lazy=True)
    phieuDatPhong = relationship('PhieuDatPhong', backref='phieu', lazy=True)
    hoaDon = relationship('HoaDon', backref='phieu', lazy=True, uselist=False)


class PhieuThuePhong(db.Model):
    __tablename__ = "phieuthuephong"
    id = db.Column(db.Integer, ForeignKey('phieu.id'),primary_key=True, autoincrement=True, nullable=False)
    ngayNhanPhong = db.Column(db.DateTime, nullable=False)
    ngayTraPhong = db.Column(db.DateTime, nullable=False)
    idPhieuDatPhong = db.Column(db.Integer, ForeignKey('phieudatphong.id'),nullable=True, unique = True)
    trangThai = db.Column(db.Enum('Đang sử dụng','Đã trả phòng'), nullable=True)
    phieuThuePhong_Phong = relationship('PhieuThuePhong_Phong', backref='phieuthuephong', lazy=True)
    phieu_khachhang = relationship('Phieu_KhachHang', backref='phieuthuephong', lazy=True)


class PhieuThuePhong_Phong(BaseModel):
    __tablename__ = "phieuthuephong_phong"
    idPhong = db.Column(db.Integer, ForeignKey('phong.id'),nullable=False)
    idPhieuThuePhong = db.Column(db.Integer, ForeignKey('phieuthuephong.id'),nullable=False)
    phieuthuephong_phong_khachhang = relationship('PhieuThuePhong_Phong_KhachHang', backref = 'phieuthuephong_phong', lazy=True)


class HoaDon(BaseModel):
    __tablename__ = "hoadon"
    tongTien = db.Column(db.Double, nullable=False)
    trangThai = db.Column(db.Boolean, nullable=False, default = False)
    idPhieu = db.Column(db.Integer, ForeignKey('phieu.id'), nullable=False, unique = True)
    thoiGianTao = db.Column(db.DateTime, nullable=False, default = datetime.now())


class TaiKhoan(BaseModel, UserMixin):
    __tablename__ = "taikhoan"
    tenDangNhap = db.Column(db.String(50), nullable=False)
    matKhau = db.Column(db.String(50), nullable=False)
    soDienThoai = db.Column(db.String(10), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    thoiGianTao = db.Column(db.DateTime, nullable=False, default = datetime.now())
    idLoaiTaiKhoan = db.Column(db.Integer, ForeignKey('loaitaikhoan.id'), nullable=False, info={"unsigned": True}, default= 2)
    idKhachHang = db.Column(db.Integer, ForeignKey('khachhang.id'), nullable=True, info={"unsigned": True}, unique = True)


class LoaiTaiKhoan(BaseModel):
    __tablename__ = "loaitaikhoan"
    tenLoaiTaiKhoan = db.Column(db.String(50), nullable=False)
    taikhoan = relationship('TaiKhoan', backref='loaitaikhoan', lazy=True)
    def __str__(self):
        return self.tenLoaiTaiKhoan


class Phieu_KhachHang(BaseModel):
    __tablename__ = "phieu_khachhang"
    idKhachHang = db.Column(db.Integer, ForeignKey('khachhang.id'), nullable=False, info={"unsigned": True})
    idPhieu = db.Column(db.Integer, ForeignKey('phieuthuephong.id'), nullable=False, info={"unsigned": True})


class PhieuDatPhong(db.Model):
    __tablename__ = "phieudatphong"
    id = db.Column(db.Integer, ForeignKey('phieu.id'), primary_key=True, autoincrement=True, nullable=False)
    idKhachHang = db.Column(db.Integer, ForeignKey('khachhang.id'), nullable = False)
    idLoaiPhong = db.Column(db.Integer, ForeignKey('loaiphong.id'), nullable=False)
    soLuong = db.Column(db.Integer, nullable=False)
    trangThai = db.Column(db.Enum('Đã nhận phòng', 'Chưa nhận phòng', 'Đã hủy'), nullable=True, default = 'Chưa nhận phòng')
    ngayNhanPhong = db.Column(db.DateTime, nullable=True)
    ngayTraPhong = db.Column(db.DateTime, nullable=True)


class LoaiKhach(BaseModel):
    __tablename__ = "loaikhach"
    tenLoaiKhach = db.Column(db.String(50), nullable=False)
    heSo = db.Column(db.Double, nullable=False)
    khachhang = relationship('KhachHang', backref='loaikhach', lazy=True)
    def __str__(self):
        return self.tenLoaiKhach

class PhieuThuePhong_Phong_KhachHang(BaseModel):
    __tablename__ = "phieuthuephong_phong_khachhang"
    idKhachHang = db.Column(db.Integer, ForeignKey('khachhang.id'), nullable=False)
    idPhieuThuePhong_Phong = db.Column(db.Integer, ForeignKey('phieuthuephong_phong.id'), nullable=False)
    trangThai = db.Column(db.Enum('Đã nhận phòng','Đã trả phòng'), nullable = False, default='Đã nhận phòng')


if __name__ == '__main__':
    with app.app_context():
        # db.create_all()
        app.run(debug = True)

