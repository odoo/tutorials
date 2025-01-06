from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _order = 'name desc'

    name = fields.Char(string="name", required=True)
    color = fields.Integer()

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'The property tag name must be unique')
    ]
