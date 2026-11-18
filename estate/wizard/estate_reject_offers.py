from odoo import fields, models


class EstateRejectOffers(models.TransientModel):
    _name = "estate.property.reject.offers"
    _description = "Reject offers of a property"

    minimum_price = fields.Integer()

    def action_reject_offers(self):
        active_id = self.env.context.get("active_id")
        offers = self.env['estate.property.offers'].search(
            [('property_id', "=", active_id), ('price', '<=', self.minimum_price)])
        offers.status = 'refused'
