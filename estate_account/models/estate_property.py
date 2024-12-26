from odoo import fields, Command, models

class EstateProperty(models.Model):
    _inherit = 'estate.property'
    _description = 'Inherited estate property model'

    def action_set_sold(self):
        for record in self:
            record.check_access('create')
            invoice_vals = {
                        'move_type': 'out_invoice',  
                        'partner_id': record.partner_id.id,  
                        'invoice_date': fields.Date.today(),  
                        'invoice_line_ids': [
                            Command.create(
                                {
                                    "name": record.display_name,
                                    "quantity": 1,
                                    "price_unit": record.selling_price
                                }
                            ),
                            Command.create(
                                {
                                    "name": '"6%" of Property Sale Price',
                                    "quantity": 1,
                                    "price_unit": record.selling_price * 0.06,
                                }
                            ),
                            Command.create(
                                {
                                    "name": "Administrative Fees",
                                    "quantity": 1,
                                    "price_unit": 100,
                                }
                            ),
                        ],
                    }
            self.env["account.move"].sudo().create(invoice_vals)
        return super().action_set_sold()
