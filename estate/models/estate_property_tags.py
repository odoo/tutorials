from odoo import fields,models

class estatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "tags for the property"
    _order = "name"

    name = fields.Char("Property Tag", required=True)

    _sql_constraints = [("check_unique_property_tag", "UNIQUE(name)", "Property Tags must be unique")]

    color = fields.Integer(default = 1)
