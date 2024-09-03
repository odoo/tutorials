from odoo import models, fields


class EstatePropertyOfferWizard(models.TransientModel):
    _name = 'estate.property.offer.wizard'
    _description = 'Estate Property offer wizard'

    price = fields.Float(string='Offer Price', required=True)
    validity = fields.Integer(default=7)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)

    def make_offer(self):
        active_ids = self.env.context.get('active_ids')
        properties = self.env['estate.property'].browse(active_ids)
        for prop in properties:
            prop.state = "offer_received"
            self.env['estate.property.offer'].create({
                'property_id': prop.id,
                'price': self.price,
                'validity': self.validity,
                'partner_id': self.partner_id.id,
            })
        return {'type': 'ir.actions.act_window_close'}
