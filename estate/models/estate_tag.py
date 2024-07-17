from odoo import fields, models

class EstateTagModel(models.Model):
    _name = 'estate.property.tag'
    _description = "Real estate property tags"
    _order = 'name'
    _sql_constraints = [('check_name', 'UNIQUE(name)', "The name must be unique.")]

    name = fields.Char(required=True)
    color = fields.Integer()
