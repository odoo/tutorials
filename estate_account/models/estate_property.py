from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _inherit = ["estate.property"]

    def sold_estate_property(self):
        for record in self:
            invoice_vals = {'partner_id': record.buyer_id.id, 'move_type': 'out_invoice', 'journal_id': 1,
                'invoice_line_ids': [
                    fields.Command.create({'name': record.name, 'quantity': 1, 'price_unit': (6 / 100) * record.selling_price}),
                    fields.Command.create({'name': 'Administrative fees', 'quantity': 1, 'price_unit': 100})]}
            self.env['account.move'].create(invoice_vals)

        return super().sold_estate_property()
