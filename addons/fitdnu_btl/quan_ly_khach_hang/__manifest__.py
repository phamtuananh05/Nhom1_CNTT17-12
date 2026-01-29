# -*- coding: utf-8 -*-
{
    'name': 'Quản lý khách hàng',
    'version': '15.0.1.0.0',
    'category': 'Sales',
    'summary': 'Quản lý thông tin khách hàng',
    'description': 'Module quản lý khách hàng phục vụ hoạt động bán hàng',
    'author': 'FIT-DNU',
    'depends': [
        'base',
        'quan_ly_nhan_su'
    ],
    'data': [
    'security/ir.model.access.csv',
    'views/khach_hang_view.xml',  # action ở đây
    'views/menu.xml',             # menu gọi action
],
    'application': True,
}
