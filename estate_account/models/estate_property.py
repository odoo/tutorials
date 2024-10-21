from odoo import models, Command
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def set_property_to_sold(self):
        self.ensure_one()

        cid = self.env.company.id
        journal = self.env['account.journal'].search(
            domain=[
                *self.env['account.journal']._check_company_domain(cid),
                ('type', '=', 'sale'),
            ],
            limit=1,
        )
        if not journal:
            raise UserError('Please define an accounting sales journal for the company %s (%s).') % (self.company_id.name, self.company_id.id)

        invoice_vals = {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            'journal_id': journal.id,
            'invoice_line_ids': [
                Command.create({
                    "name": "Commission",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06
                }),
                Command.create({
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100.00

                })
            ]
        }

        self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals)

        return super().set_property_to_sold()
