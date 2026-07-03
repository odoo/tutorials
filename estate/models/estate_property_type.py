from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name"

    name = fields.Char(string="Type", required=True)
    sequence = fields.Integer(string="Sequence", default=1)
    property_ids = fields.One2many("estate.property", "property_type_id")

    _check_name = models.Constraint("UNIQUE(name)", "Type name must be unique")
