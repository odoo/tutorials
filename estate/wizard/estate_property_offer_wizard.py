from odoo import models, fields

class estate_property_offer_wizard(models.TransientModel):
    _name = "estate.property.offer.wizard"  
    _description = "Make an offer wizard for multiple properties"

    price = fields.Float()
    validity = fields.Integer(default=7)
    buyer = fields.Many2one("res.partner", copy=False)
    
    def make_an_offer(self):
        properties = self.env['estate.property'].browse(self._context.get("records", []))
        for property in properties:
            self.env['estate.property.offer'].create({
                'price': self.price,
                'property_id': property.id,
                'validity': self.validity,
                'partner_id': self.buyer.id,
            })

        return {'type': 'ir.actions.act_window_close'}