from calendar import month
from datetime import datetime
from urllib import request

from flask import redirect, request
from flask.views import MethodView
from flask_admin.contrib.sqla.fields import QuerySelectField
from flask_admin.form import Select2Widget
from sqlalchemy import ForeignKey

import utils
from qlkswebsite import db
from qlkswebsite import app
from qlkswebsite.models import KhachHang, TaiKhoan, LoaiTaiKhoan, LoaiKhach, Phong, LoaiPhong, TyLePhuThu, BaseModel
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_login import logout_user, current_user

from qlkswebsite.utils import tuansuatsudung


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        stats = tuansuatsudung()
        return self.render('admin/index.html', stats=stats)


admin = Admin(app=app, name='Hệ Thống Quản Lý Khách', template_mode='bootstrap4', index_view=MyAdminIndex())


class TaiKhoanModelView(ModelView):
    form_columns = ['tenDangNhap', 'matKhau', 'soDienThoai', 'email', 'thoiGianTao', 'idLoaiTaiKhoan']

    # form_widget_args = {
    #     'idLoaiTaiKhoan': {
    #         'widget': Select2Widget()
    #     }
    # }
    #     #     'idKhachHang': {
    #     #         'widget': Select2Widget()
    #     #     }
    #     # }
    #     #
    #     form_extra_fields = {
    #         'idLoaiTaiKhoan': QuerySelectField(
    #             'Loại Tài Khoản',
    #             query_factory=lambda: db.session.query(LoaiTaiKhoan).all(),
    #             get_label=lambda c: c.tenLoaiTaiKhoan,
    #             allow_blank=True
    #         )
    #     }
    #     #     'idKhachHang': QuerySelectField(
    #     #         'Khách Hàng',
    #     #         query_factory=lambda: db.session.query(KhachHang).all(),
    #     #         get_label=lambda c: c.tenKhachHang,
    #     #         allow_blank=True
    #     #     )
    #     # }
    #
    # def on_model_change(self, form, model, is_created):
    #     if is_created:
    #         model.idLoaiTaiKhoan = form.idLoaiTaiKhoan.data
    #         model.idKhachHang = form.idKhachHang.data
    #     return super().on_model_change(form, model, is_created)

    # Cách để tạo một dropdown tùy chỉnh cho khóa ngoại
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.idLoaiTaiKhoan = form.idLoaiTaiKhoan.data
        return super().on_model_change(form, model, is_created)


#

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)

        return self.render('admin/stats.html', month_stats=utils.doanhthuthang_stats(year=year),
                           stats=utils.baocaodoanhthu_stats(kw=kw, from_date=from_date, to_date=to_date))

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(ModelView(KhachHang, db.session, name="Khách Hàng"))
admin.add_view(ModelView(LoaiKhach, db.session, name="Loại Khách"))
admin.add_view(TaiKhoanModelView(TaiKhoan, db.session, name="Tài Khoản", endpoint='tai_khoan'))
admin.add_view(ModelView(Phong, db.session, name="Phòng"))
admin.add_view(ModelView(LoaiPhong, db.session, name="Lọai Phòng"))
admin.add_view(ModelView(TyLePhuThu, db.session, name="Tỷ lệ Phụ Thu"))
admin.add_view(StatsView(name='Stats'))
admin.add_view(LogoutView(name="Đăng Xuất"))

