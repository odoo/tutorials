from odoo import models, fields


class PropertyTag(models.Model):
    _name = "public.property.tag"
    _description = "Property Tags"
    _order = "name"
    name = fields.Char(required=True)
    color = fields.Integer(string="Color")
    _sql_constraints = [
        ("uniq_property_tag", "unique(name)", "A property tag must be unique.")
    ]
