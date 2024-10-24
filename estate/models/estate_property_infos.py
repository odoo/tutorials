from odoo import fields, models


class Estate_Property_Type(models.Model):
    _name = "estate_property_type"
    _description = "Estate property Types"
    _order = "name"

    name = fields.Char(
        required=True,
        string="Type"
    )

    property_ids = fields.One2many(
        "estate_property",
        "type_id",
        string="Estate Properties"
    )

    _sql_constraints = [
        ("check_unique_type", "UNIQUE(name)", "Property types must be unique.")
    ]


class Estate_Property_Tag(models.Model):
    _name = "estate_property_tag"
    _description = "Estate property Tags"
    _order = "name"

    name = fields.Char(
        required=True,
        string="Type"
    )

    property_estate_ids = fields.Many2many(
        "estate_property",
        string="Estate Properties"
    )

    _sql_constraints = [
        ("check_unique_tag", "UNIQUE(name)", "Property tags must be unique.")
    ]
