# -*- coding: utf-8 -*-

from odoo import _, api, exceptions, fields, models
from odoo.exceptions import UserError, ValidationError
import math

class AccountPayment(models.Model):
    """Added custom fields bank_fee and include_fee_in_payment to add the extra charges"""
    _inherit = "account.payment"

    bank_fee = fields.Monetary(
        string="Bank Fee Amount", 
        currency_field='currency_id')
    include_fee_in_payment = fields.Selection(
        string="Bank Fee", 
        selection=[
            ("included", "Fee Included"),
            ("excluded", "Fee Excluded"),
        ],
        default="included",
        tracking=True,
        help="Select wither to includ bank fee in the same journal\n"
        "Fee included: Deduct the banke fee from the amount\n"
        "Fee Excluded: Add the bank fee as an extra amout.",
    )

    def _prepare_move_line_default_vals(self, write_off_line_vals=None):
        """Adding bank charges in move line"""
        res = super(AccountPayment, self)._prepare_move_line_default_vals(write_off_line_vals=write_off_line_vals)
        if self.bank_fee and self.bank_fee > 0:
            original_amount = self.amount
            net_amount = original_amount - self.bank_fee
            # Get the payable bank fees account configured for the company
            if not self.company_id.bank_fees_account_id:
                raise UserError('Bank Fees and Charges Account is not configured for this company.')

            # Get the journal entry associated with the payment
            move = self.move_id  
            debit_line = None
            credit_line = None
            bank_fee_debit_line = None
            bank_fee_credit_line = None
            for line in res:
                if line['debit'] > 0.0:
                    debit_line = line
                    bank_fee_debit_line = line.copy()  # Create a copy of the debit line
                elif line['credit'] > 0.0:
                    credit_line = line
                    bank_fee_credit_line = line.copy()  # Create a copy of the credit line

            # create a seperate journal entries for bank & bank fees
            if self.include_fee_in_payment=='included' and debit_line:
                # deduct the bank fee amount from debit entry
                debit_line.update({'debit': net_amount,'amount_currency': net_amount,})
                bank_fee_debit_line.update({'debit': self.bank_fee,'amount_currency': self.bank_fee,'account_id':self.company_id.bank_fees_account_id.id})
                res.append(bank_fee_debit_line)
            elif self.include_fee_in_payment=='excluded':
                bank_fee_credit_line.update({'credit': self.bank_fee,'amount_currency': -self.bank_fee,})
                bank_fee_debit_line.update({'debit': self.bank_fee,'amount_currency': self.bank_fee,'account_id':self.company_id.bank_fees_account_id.id})
                res.extend([bank_fee_credit_line,bank_fee_debit_line])
                

        return res
    
    def write(self, values):
        """Override write method to append lines to move when fields are changed."""
        res = super(AccountPayment, self).write(values)

        # Check if the bank_fee or include_fee_in_payment fields are being updated
        if 'bank_fee' in values or 'include_fee_in_payment' in values:
            # Ensure we are in the draft state and the move_id is present
            if self.state == 'draft' and self.move_id:
                # Generate new move lines based on the updated custom fields
                move_lines = self._prepare_move_line_default_vals()

               # Append the new lines to the existing move (journal entry)
                new_lines = []
                for line in move_lines:
                    line.update({'move_id': self.move_id.id})  # Link the new line to the existing journal
                    new_lines.append((0, 0, line))  # Prepare the line to be inserted

               # Replace the old lines with the new ones in the move
                if new_lines:
                    self.move_id.write({
                        'line_ids': [(5, 0, 0)] + new_lines  # (5, 0, 0) removes all existing lines before adding new ones
                    })
        return res