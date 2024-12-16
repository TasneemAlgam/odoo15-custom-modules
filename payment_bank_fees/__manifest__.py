# -*- coding: utf-8 -*-

{
    'name': "Account Bank Fees And Charges In Payment",
    'version': '15.0.1.0.0',
    'category': 'Accounting',
    'summary': """This Module Allows to Add Bank Fees in Payments""",
    'description': """This Module Allows to Add Separate Journal Entries for Bank Fees And Charges in Payments""",
    'author': 'Tasneem Algam',
    'company': '',
    'maintainer': '',
    'website': '',
    'depends': ['base', 'account'],
    'data': [
        'views/res_config_settings.xml',
        'views/account_payment_view.xml',
    ],
    'images': [''],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}