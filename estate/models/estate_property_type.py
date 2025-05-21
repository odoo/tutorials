from odoo import models, fields


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "the type of an estate"

    name = fields.Char("Type", required=True)

    _sql_constraints = [("unique_property_tag", "UNIQUE(name)", "Tag name must be unique !")]
