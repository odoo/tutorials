from odoo import fields, models

class AnyFlatProperty(models.TransientModel):
    _name = 'estate.property.offer.to.anyflat'
    _description = "add offer to multiple properties"

    price = fields.Float(required=True)
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    buyer_id = fields.Many2one(
        'res.partner',
        required=True
    )

    def add_offer_to_selected_flats(self):
        property_ids = self.env.context['active_ids']
        properties =  self.env['estate.property'].browse(property_ids)
        for property in properties:
            self.env['estate.property.offer'].create(
                {
                    'price': self.price,
                    'status': self.status,
                    'partner_id': self.buyer_id.id,
                    'property_id': property.id
                }
            )
