from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "A tag used to describe a property"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

    _sql_constraints = [("unique_name", "unique (name)", "A tag with this name already exist.")]
