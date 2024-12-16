# -*- coding: utf-8 -*-

from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    # used for bank fee deductions
    bank_fees_account_id = fields.Many2one(
        'account.account', 
        string='Bank Fees Account', 
    )