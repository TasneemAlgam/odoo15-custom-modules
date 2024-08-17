# -*- coding: utf-8 -*-

{
    'name': 'Employee Expenses Dashboard',
    'version': '15.0.1.0.0',
    'category': 'HR',
    'summary': """Employee Expenses Dashboard In Odoo Portal""",
    'description': """Employee Expenses Dashboard In Odoo Portal""",
    'author': 'Tasneem Algam',
    'depends': ['portal', 'hr_expense'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/expenses_dashboard.xml',
        'views/portal_employee_expense.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'employee_expenses_portal/static/src/js/expenses_dashboard.js',
        ],
        'web.assets_frontend': [
            'employee_expenses_portal/static/src/css/styles.css',
        ],
        'web.assets_qweb': [
            'employee_expenses_portal/static/src/xml/**/*',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
