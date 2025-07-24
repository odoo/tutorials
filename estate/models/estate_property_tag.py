from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _order = "name"
    name = fields.Char(required = True)
    color = fields.Integer()



    _sql_constraints = [
        ('is_tag_unique', 'UNIQUE(name)', 'Tag name must be unique!')
    ]