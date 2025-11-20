from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char(required=True)


class PropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"

    name = fields.Char(required=True)


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _descrption = "Estate Property Offer"

    price = fields.Float(required=True)
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", required="True")
    property_id = fields.Many2one("estate.property", string="Property", required="True")
