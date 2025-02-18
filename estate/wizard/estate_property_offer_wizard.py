from odoo import fields, models

class EstatePropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "Estate Property Offer Wizard"

    price = fields.Float(string="Offer Price", required=True)
    validity = fields.Integer(string="Validity (in days)", default=7)
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)

    def action_add_offer(self):
        property_ids = self.env.context.get('active_ids')
        for property_id in property_ids:
            self.env['estate.property.offer'].create({
                'property_id': property_id,
                'price': self.price,
                'validity': self.validity,
                'partner_id': self.partner_id.id,
            })
        return {'type': 'ir.actions.act_window_close'}
        
