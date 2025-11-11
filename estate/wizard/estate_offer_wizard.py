from odoo import fields, models


class EstateOfferWizard(models.Model):
    _name = "estate.offer.wizard"
    _description = "create offer for multiple property at a time"

    price = fields.Float(string="Price", required=True)
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)

    def action_make_offer(self):
        property_ids = self.env.context.get('active_ids', [])
        properties = self.env['estate.property'].browse(property_ids)

        for property in properties:
            self.env['estate.property.offer'].create(
                {
                    'price': self.price,
                    'partner_id': self.partner_id.id,
                    'validity': self.validity,
                    'property_id': property.id
                }
            )
