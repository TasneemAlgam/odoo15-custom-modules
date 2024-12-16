# -*- coding: utf-8 -*-

from odoo import models, api
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    ''' overwriting the write() function of account move which calles the  _synchronize_business_models()
     that calles _synchronize_from_moves() which has the condition :
        if len(liquidity_lines) != 1:
            raise UserError(_(
                "Journal Entry %s is not valid. In order to proceed, the journal items must "
                "include one and only one outstanding payments/receipts account.",
                move.display_name,
                    ))
    which we are going to invoc when we create two Outstanding Bank Payments in ower customized entries              
    '''
    @api.model
    def write(self, vals):
        res = super(AccountMove, self.with_context(skip_account_move_synchronization=True)).write(vals)
        
        # For each move, check if the related payment exists and if its 'bank_fees'  is 'excluded'
        related_payment = self.mapped('payment_id') 
        if not (related_payment.bank_fee > 0 and related_payment.include_fee_in_payment == 'excluded'):
            # Skip synchronization if bank_fee amount is > o and 'include_fee_in_payment' is 'excluded' 
            self._synchronize_business_models(set(vals.keys()))

        return res