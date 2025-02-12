from odoo import models,fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'for listing property types'
    _order = 'name'

    name = fields.Char(string='Name',required=True)
    color = fields.Integer("Color_Index")

    _sql_constraints =[
        ('unique_tag_name', 'UNIQUE(name)', 'A property tag name must be unique')
    ]
