from odoo import models


class Estate_property(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        for record in self:
            invoice_line_ids = [
                                    (0,0,{
                                        'name':'6% of the total price',
                                        'quantity':1,
                                        'price_unit':record.selling_price * 0.06
                                        }),
                                    (0,0,{
                                        'name':'Administrative fees',
                                        'quantity':1,
                                        'price_unit':100
                                        }),
                                    
                                ]
            info = {
                'partner_id':record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': invoice_line_ids
            }
            record.env['account.move'].create(info)
            return super().action_set_sold()
