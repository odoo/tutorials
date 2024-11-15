from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.types"
    _description = "Real Estate Property Type"
    _order = "sequence, name, id"

    name = fields.Char(required=True, string="Property Type")

    _sql_constraints = [
        ("check_property_type", "UNIQUE(name)", "Property type must be unique"),
    ]

    property_ids = fields.One2many("estate.property", "propery_type_id")

    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")