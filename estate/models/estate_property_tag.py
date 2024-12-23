from odoo import fields,models

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'real estate property tag'

    name= fields.Char(required=True)
    color=fields.Integer(required=True)
    _order = "create_date desc"

    _sql_constraints = [('check_unique_name', 'UNIQUE(name)', 'Property tag name must be unique.')]
