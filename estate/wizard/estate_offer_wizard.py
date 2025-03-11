from odoo import models, fields
from odoo.exceptions import UserError

class EstateOfferWizard(models.TransientModel):
    _name = 'estate.offer.wizard'
    _description = 'Add Offer Wizard'

    property_ids = fields.Many2many('estate.property', string='Properties', required=True)
    price = fields.Float(string='Price', required=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    validity = fields.Integer(string="Validity", default=7)

    def action_make_offer(self):
        active_property_ids = self.env.context.get('active_ids', [])
        if not active_property_ids:
            raise UserError("No properties selected") 
        selected_properties = self.env['estate.property'].browse(active_property_ids)
        offer_values = []
        for property_id in selected_properties:
            offer_values.append({
                'property_id': property_id.id,
                'price': self.price,
                'partner_id': self.partner_id.id,
                'validity': self.validity,
            })
        self.env['estate.property.offer'].create(offer_values)
