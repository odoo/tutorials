from odoo import fields, models


class propertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for the Real Estate Property"
    _order = "name"

    name = fields.Char("Tags", required=True)
    color = fields.Integer("Color")

    _sql_constraints = [('name_uniq', "unique(name)", "Name of Property Tag must be Unique")]
