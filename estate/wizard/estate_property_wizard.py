from odoo import fields, models


class OfferWizard(models.TransientModel):
    _name = "property.offer.wizard"
    _description = "estate property offer wizard"

    price = fields.Float()
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    validity = fields.Integer(default=7)
    property_ids = fields.Many2many("estate.property")

    def action_make_property_offer(self):
        context = self.env.context
        active_ids = context.get('active_ids', [])
        for property_id in active_ids:
            property = self.env['estate.property'].browse(property_id)
            self.env['estate.property.offer'].create({
                'price': self.price,
                'validity': self.validity,
                'partner_id': self.partner_id.id,
                'property_id': property.id,
            })
