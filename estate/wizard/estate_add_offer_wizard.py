from odoo import models, fields, api
from odoo.exceptions import UserError


class EstateAddOfferWizard(models.TransientModel):
    _name = 'estate.add.offer.wizard'
    _description = 'Wizard for Adding Offers to Properties'

    price = fields.Float(string="Offer Price", required=True)
    buyer_id = fields.Many2one('res.partner', string="Buyer", required=True)
    offer_status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Offer Status",
        required=True
    )

    def make_offer(self):
        property_ids = self.env.context.get('active_ids')
        properties = self.env['estate.property'].browse(property_ids)
        
        if not properties:
            raise UserError("No properties selected.")
        
        for property in properties:
            self.env['estate.property.offer'].create({
                'price': self.price,
                'partner_id': self.buyer_id.id,
                'property_id': property.id,
                'status': self.offer_status
            })
