from odoo import models, fields

class EstateOfferWizard(models.TransientModel):
    _name = 'estate.offer.wizard'
    _description = 'Wizard to Add Offer to Properties'

    price = fields.Float(string="Price", required=True)
    validity = fields.Integer(string="Validity (Days)", default=7)
    buyer_id = fields.Many2one('res.partner', string="Buyer", required=True)

    def make_offer(self):
        property_ids = self.env.context.get('default_property_ids', [])
        for property in property_ids:
            self.env['estate.property.offer'].create({
                'price': self.price,
                'validity': self.validity,
                'buyer_id': self.buyer_id.id,
                'property_id': property,
            })
        return {'type': 'ir.actions.act_window_close'}
