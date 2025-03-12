from odoo import fields, models
from odoo.exceptions import UserError


class OfferMultiProperty(models.TransientModel):
    _name = 'estate.offer.multi.property.wizard'
    _description = "To make offer for multiple properties"

    price = fields.Float(string="Price", required=True)
    validity = fields.Integer(string="Validity", default=7, required=True)
    buyer_id = fields.Many2one(comodel_name='res.partner', string="Buyer", required=True)

    def action_make_offer(self):
        active_ids = self.env.context.get('active_ids', [])

        if not UserError:
            raise UserError("At least one property should be selected.")
        properties = self.env['estate.property'].browse(active_ids)
        property_offer_obj = self.env['estate.property.offer']
        
        offers = [{
            'property_id': property.id,
            'price': self.price,
            'validity': self.validity,
            'partner_id': self.buyer_id.id
        } for property in properties]

        property_offer_obj.create(offers)
