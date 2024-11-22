from odoo import models, fields # type: ignore

class estate_property_tag(models.Model):
    _name = "estate.property.tag"  
    _description = "real estate property tags"

    name = fields.Char(required=True)

    _sql_constraints = [
        ('code_tag_uniq', 'unique (name)', 'Tag name must be unique.'),
    ]