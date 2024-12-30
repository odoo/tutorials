from odoo import fields, models

class EstateMultipleOffer(models.TransientModel):
    _name = 'estate.multiple.offer'
    _description = 'Enable making offer for multiple properties at once'

    price = fields.Float()
    partner_id = fields.Many2one('res.partner', required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    
    _sql_constraints = [('check_price', 'CHECK(price>=0)', 'Offer price price must be positive.')]
    
    # Logic to add details from transient model to actual offer model
    def action_make_offer(self):
        """Make an offer for the selected properties."""
        property_ids = self.env.context.get("default_property_ids", [])
        Offer = self.env['estate.property.offer']
        for property in property_ids:
            Offer.create({
                'property_id': property,
                'price': self.price,
                'partner_id': self.partner_id.id,
                'validity': self.validity,
            })
        return {'type': 'ir.actions.act_window_close'}
