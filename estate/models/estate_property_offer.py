from odoo import fields, models

OFFER_STATUS = [
    ('accepted', 'Accepted'),
    ('refused', 'Refused'),
]


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An estate property offer model"

    # === FIELDS ===#

    price = fields.Float()
    status = fields.Selection(
        selection=OFFER_STATUS,
        copy=False)
    partner_id = fields.Many2one(
        "res.partner",
        string='Partner',
        required=True)
    property_id = fields.Many2one(
        "estate.property",
        string='Property',
        required=True)
