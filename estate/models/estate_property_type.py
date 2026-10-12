from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property Type"

    name = fields.Char(string="Type", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")

    _unique_tag_name = models.Constraint("UNIQUE(name)", "Tag name must be unique.")
