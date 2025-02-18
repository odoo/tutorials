from odoo import fields,models,api

class MakeAnOffer(models.TransientModel):
    _name="estate.property.wizard_offer"
    _description="This wizard handles the make an offer button"

    price = fields.Float(string="Price", required=True)
    validity = fields.Integer(string="Validity (Days)")
    partner_id = fields.Many2one('res.partner', string="Buyer")

    def make_an_offer(self):
        property_ids = self.env.context.get('active_ids', [])
        for property_id in property_ids:
            self.env['estate.property.offer'].create({
                'property_id': property_id,
                'price': self.price,
                'validity': self.validity,
                'partner_id': self.partner_id.id,
            })
            
