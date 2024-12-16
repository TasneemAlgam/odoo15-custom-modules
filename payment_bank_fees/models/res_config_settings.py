# -*- coding: utf-8 -*-

from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # from the requirments document i assumed that bank fees and charges has its one account and the type of it is expenses
    bank_fees_account_id = fields.Many2one(
        'account.account',
        string='Bank Fees and Charges Account',
        readonly=False,
        related='company_id.bank_fees_account_id',
        domain=lambda self: "[('internal_type', '=', 'other'), ('deprecated', '=', False), ('company_id', '=', company_id),\
                             ('user_type_id', '=', %s)]" % self.env.ref('account.data_account_type_expenses').id,
        help="Account used to record payable bank fees for this company.",
    )