from odoo import models, api


class KhachHang(models.Model):
    _inherit = 'khach_hang'

    def _tao_cong_viec_cham_soc(self):
        for record in self:
            existing_task = self.env['cong_viec'].search([
                ('mo_ta', 'ilike', record.ten_khach_hang),
            ], limit=1)

            if existing_task:
                continue

            self.env['cong_viec'].create({
                'ten_cong_viec': f'Chăm sóc khách hàng {record.ten_khach_hang}',
                'nhan_vien_ids': [(6, 0, [record.nhan_vien_phu_trach_id.id])],
                'mo_ta': f'Tự động tạo khi chăm sóc khách hàng {record.ten_khach_hang}'
            })
