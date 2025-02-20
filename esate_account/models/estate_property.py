from odoo import Command, api, models
from odoo.exceptions import ValidationError, AccessError


class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def action_set_sold(self):
        
        try:
            self.check_access('write')
            self.env['account.move'].check_access_rights('create', raise_exception=True)
        except AccessError:
            raise ValidationError('Access nahi hai')
        res = super().action_set_sold()
        if not self.buyer_id:
            raise ValidationError("No buyer assigned! Cannot create an invoice.")
        journal = self.env['account.journal'].sudo().search([
            ('type', '=', 'sale'),
            ('company_id', '=', self.company_id.id)
        ], limit=1)
        if not journal:
            raise UserError(f"No sales journal found for company {self.company_id.name}. Please ensure there is a journal of type 'Sale'.")
        self.env['account.move'].sudo().create({
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            'company_id': self.company_id.id, 
            'invoice_line_ids': [
                Command.create({
                    'name': "6% of the selling price",
                    'quantity': '1',
                    'price_unit': self.selling_price * 0.06
                }),
                Command.create({
                    'name': "Administrative fees",
                    'quantity': '1',
                    'price_unit':100
                })
            ]
        })
        return res
