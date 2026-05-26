from odoo import Command, models


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"


    def action_accept(self):
        sale = super().action_accept()
        for record in self:
            self.env['sale.order'].create({
                'partner_id': record.partner_id.id,
                'order_line': [
                    Command.create({
                        'name': f' Offer by {record.partner_id.name} on{record.property_id.name}',
                        'product_uom_qty': 1,
                        'price_unit': record.price
                    })
                ]
            })
        
        return sale
    
