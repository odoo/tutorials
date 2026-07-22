from odoo import Command, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _inherit = "estate.property"

    def action_sold(self):
        self._create_invoices()
        return super().action_sold()

    def _prepare_invoice(self):
        self.ensure_one()
        return {
            'partner_id': self.buyer_id.id,
            'move_type': 'out_invoice',
            # 'journal_id':,
            'invoice_line_ids': [
                Command.create({
                    'name': '6% of selling price',
                    'quantity': 1,
                    'price_unit': 0.06 * self.selling_price,
                }),
                Command.create({
                    'name': 'Administrative fee',
                    'quantity': 1,
                    'price_unit': 100.00,
                }),
            ],
        }

    def _create_invoices(self):
        self.env['account.move'].check_access('create')

        for property in self:
            invoice_values = property._prepare_invoice()
            self.env['account.move'].with_context(default_move_type='out_invoice').create(invoice_values)
