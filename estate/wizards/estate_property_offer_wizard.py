from datetime import timedelta

from odoo import models, fields
from odoo.exceptions import UserError


class EstatePropertyOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'Wizard allowing to add offers for the property'

    price = fields.Float(required = True)
    buyer_id = fields.Many2one('res.partner', string='Buyer')
    date_deadline = fields.Date("Deadline", default=lambda self: fields.Date.today() + timedelta(days=7))

    def action_add_offer(self):
        properties = self.env['estate.property'].browse(self.env.context.get('active_ids', []))
        for estate_property in properties:
            if estate_property.state == 'sold':
                raise UserError(f"The property '{estate_property.name}' is sold ")
            elif estate_property.state == 'offer_accepted':
                raise UserError(f"The property '{estate_property.name}' has a offer accepted")
            self.env['estate.property.offer'].create({
                'price' : self.price,
                'partner_id' : self.buyer_id.id,
                'date_deadline':self.date_deadline,
                'property_id' : estate_property.id
            })
        return {'type': 'ir.actions.act_window_close'}
