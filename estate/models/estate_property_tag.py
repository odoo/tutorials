from odoo import fields, models


class PropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Tags used to describe a property"

    name = fields.Char("name", required=True)

    _sql_constraints = [("unique_property_tag", "UNIQUE(name)", "Tag name must be unique !")]
