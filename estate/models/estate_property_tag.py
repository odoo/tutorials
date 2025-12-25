from odoo import fields, models

class EstatePropertyTag(models.Model):
    '''Estate property tag'''
    _name = "estate.property.tag"
    _description = "Tag of a property"
    _order = "name"

    name = fields.Char(required=True, string="Tag")
    color = fields.Integer("Color")

    _sql_constraints = [('unique_tag', 'unique(name)', 'The tag already exist !')]
