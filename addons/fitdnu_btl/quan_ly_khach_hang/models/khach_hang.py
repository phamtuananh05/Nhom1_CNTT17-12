from odoo import models, fields, api


class KhachHang(models.Model):
    _name = 'khach_hang'
    _description = 'Khách hàng'
    _rec_name = 'ten_khach_hang'

    ten_khach_hang = fields.Char(string='Tên khách hàng', required=True)
    dien_thoai = fields.Char(string='Số điện thoại')
    email = fields.Char(string='Email')
    dia_chi = fields.Text(string='Địa chỉ')

    nhan_vien_phu_trach_id = fields.Many2one(
        'nhan_vien',
        string='Nhân viên phụ trách',
        required=True
    )

    trang_thai = fields.Selection(
        [
            ('moi', 'Mới'),
            ('dang_cham_soc', 'Đang chăm sóc'),
            ('da_chot', 'Đã chốt'),
            ('huy', 'Hủy')
        ],
        string='Trạng thái',
        default='moi'
    )

    ghi_chu = fields.Text(string='Ghi chú')

    # ===============================
    # NGHIỆP VỤ HỘI NHẬP – MỨC 2
    # ===============================

    def _tao_cong_viec_cham_soc(self):
        """Tạo công việc chăm sóc khách hàng"""
        CongViec = self.env['cong_viec']
        DuAn = self.env['du_an']

        # tìm hoặc tạo dự án mặc định
        du_an = DuAn.search([('ten_du_an', '=', 'Chăm sóc khách hàng')], limit=1)
        if not du_an:
            du_an = DuAn.create({
                'ten_du_an': 'Chăm sóc khách hàng'
            })

        for record in self:
            # tránh tạo trùng công việc
            da_ton_tai = CongViec.search([
                ('ten_cong_viec', '=', f"Chăm sóc khách hàng {record.ten_khach_hang}"),
                ('du_an_id', '=', du_an.id),
            ], limit=1)
            if da_ton_tai:
                continue

            # đảm bảo nhân viên thuộc dự án (tránh lỗi constraint)
            if record.nhan_vien_phu_trach_id not in du_an.nhan_vien_ids:
                du_an.nhan_vien_ids = [(4, record.nhan_vien_phu_trach_id.id)]

            # tạo công việc
            CongViec.create({
                'ten_cong_viec': f"Chăm sóc khách hàng {record.ten_khach_hang}",
                'du_an_id': du_an.id,
                'nhan_vien_ids': [(6, 0, [record.nhan_vien_phu_trach_id.id])],
            })

    @api.model
    def create(self, vals):
        record = super().create(vals)

        if record.trang_thai == 'dang_cham_soc':
            record._tao_cong_viec_cham_soc()

        return record

    def write(self, vals):
        res = super().write(vals)

        if 'trang_thai' in vals and vals.get('trang_thai') == 'dang_cham_soc':
            for record in self:
                record._tao_cong_viec_cham_soc()

        return res
