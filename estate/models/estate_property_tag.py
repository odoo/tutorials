from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    name = fields.Char(required = True)

    _sql_constraints = [
        ('is_tag_unique', 'UNIQUE(name)', 'Tag name must be unique!')
    ]