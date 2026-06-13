from odoo import fields, models


class EstateOfferWizard(models.TransientModel):
    _name = 'estate.offer.wizard'
    _description = 'Estate Offer Wizard'

    price = fields.Float(string="Price")
    partner_id = fields.Many2one('res.partner', string="Buyer")

    def action_create_offer(self):
        properties = self.env['estate.property'].search([('state', '=', 'new'), ('offer_ids', '=', False)])
        for prop in properties:
            self.env['estate.property.offer'].create({
                'price': self.price,
                'partner_id': self.partner_id.id,
                'property_id': prop.id,
            })
