from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tags"
    _order = "name"

    name = fields.Char(string="Tag", required=True)
    color = fields.Integer(string="Color")

    _sql_constraints = [
        ('check_property_tag', 'UNIQUE(name)', 'Property Tag Must be Unique')]
