from odoo import fields, models


class EstatePropertyOfferModel(models.Model):
    _name = "estate_property_offer"
    _description = "An offer for an estate"

    price = fields.Float()
    status = fields.Selection(string='State',
            selection=[
                ('refused', 'Refused'),
                ('accepted', 'Offer Accepted'),
            ],
            copy=False,
        )
    partner_id = fields.Many2one("res.partner", string="Buyer")
    property_id = fields.Many2one("estate_property", string="Property")
