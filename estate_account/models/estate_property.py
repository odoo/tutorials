from odoo import models, Command


class Estate_property(models.Model):
    _inherit = "estate.property"

    def action_set_sold(self):
        create_vals = []
        for record in self:
            create_vals.append({
                'partner_id':record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': 
                    [
                        Command.create(
                            {
                                'name':'6% of the total price',
                                'quantity':1,
                                'price_unit':record.selling_price * 0.06
                            }),
                        Command.create(
                            {
                                'name':'Administrative fees',
                                'quantity':1,
                                'price_unit':100
                            }),
                                    
                    ]
            })
        if create_vals:
            record.env['account.move'].create(create_vals)
        return super().action_set_sold()
