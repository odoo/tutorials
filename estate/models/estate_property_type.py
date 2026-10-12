from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Properties Type"
    _order = "sequence, name"

    name = fields.Char("Type", required=True)
    sequence = fields.Integer("Sequence")

    property_ids = fields.One2many("estate.property", "property_type_id")
    _check_tag_name = models.Constraint("unique(name)", "Type should be unique")
