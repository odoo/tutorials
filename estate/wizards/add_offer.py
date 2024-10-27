from odoo import models, fields


class addOffer(models.TransientModel):

    _name = "add.offer"
    _description = "You can add a offer directly in multiple properties."

    price = fields.Float(required=True)
    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)

    def action_make_an_offer(self):
        select_property_id = self.env.context['active_ids']
        properties = self.env["estate.property"].browse(select_property_id)

        for property in properties:
            self.env["estate.property.offer"].create({
                'price': self.price,
                'partner_id': self.partner_id.id,
                'property_id': property.id
            })

        

