from odoo import api, fields, models


class Estate_Property_Type(models.Model):
    _name = "estate_property_type"
    _description = "Estate property Types"
    _order = "name"

    sequence = fields.Integer(
        "Sequence", default=1, help="Used to order types. Lower is better."
    )

    name = fields.Char(required=True, string="Type")

    property_ids = fields.One2many(
        "estate_property", "type_id", string="Estate Properties"
    )

    offer_ids = fields.One2many(
        "estate_property_offer", "property_type_id", string="Offer IDs"
    )

    offer_count = fields.Integer(
        compute="_count_offers", default=0, string="Offers"
    )

    _sql_constraints = [
        ("check_unique_type", "UNIQUE(name)", "Property types must be unique.")
    ]

    @api.depends("offer_ids")
    def _count_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids) if record.offer_ids else 0


class Estate_Property_Tag(models.Model):
    _name = "estate_property_tag"
    _description = "Estate property Tags"
    _order = "name"

    name = fields.Char(required=True, string="Type")

    color = fields.Integer(string="Colour")

    property_estate_ids = fields.Many2many(
        "estate_property", string="Estate Properties"
    )

    _sql_constraints = [
        ("check_unique_tag", "UNIQUE(name)", "Property tags must be unique.")
    ]
