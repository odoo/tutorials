from odoo import models, fields # type: ignore

class estate_property_tag(models.Model):
    _name = "estate.property.tag"  
    _description = "real estate property tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer(string="color")

    _sql_constraints = [
        ('code_tag_uniq', 'unique (name)', 'Tag name must be unique.'),
    ]