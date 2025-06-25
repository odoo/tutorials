from odoo import api, fields, models


class PropertyOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'To create offer for multiple properties'

    price = fields.Float(string="Price", required=True)
    validity = fields.Integer(string="Validity", default=7)
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)

    def action_add_offer(self):        
        active_ids = self._context.get('active_ids')
        property_offer_vals = [{
            'price': self.price,
            'partner_id': self.buyer_id.id,
            'validity': self.validity,
            'property_id': property_id
        } for property_id in active_ids]
        self.env['estate.property.offer'].create(property_offer_vals)
