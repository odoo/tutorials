from odoo import fields, models


class AddOfferWizard(models.TransientModel):
    _name = 'estate.add.offer.wizard'
    _description = 'Add offer to properties'

    price = fields.Float(string="Price", required=True)
    validity = fields.Integer(string="Validity (days)", required=True)
    buyer_id = fields.Many2one('res.partner', string="Buyer", required=True)

    def add_offer(self):
      property_ids = self.env.context.get('active_ids', [])
      for property in self.env['estate.property'].browse(property_ids):
            self.env['estate.property.offer'].create({
                'property_id': property.id,
                'price': self.price,
                'validity': self.validity,
                'buyer_id': self.buyer_id.id
            })
