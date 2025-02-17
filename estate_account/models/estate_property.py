from odoo import models,fields,Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    invoice_id  = fields.Many2one('account.move', string="Invoice", readonly=True)
    def action_sold_property(self):
        for record in self:
            if record.selling_price > 0:
                record.invoice_id = self.env['account.move'].create(
                    {
                        'partner_id' : record.partner_id.id,
                        'move_type' : "out_invoice",
                        "invoice_line_ids": [
                            Command.create(
                                {
                                    "name": record.name,
                                    "quantity": 1.0,
                                    "price_unit": record.selling_price * 0.06,
                                },
                            ),
                            Command.create(
                                {
                                    "name": 'Administrative fees',
                                    "quantity": 1.0,
                                    "price_unit": '100',
                                },
                            ),
                        ]
                    }
                )
        return super().action_sold_property()