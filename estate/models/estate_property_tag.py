from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = 'estate_property_tag'
    _description = "Estate property tag"
    _order = "name"

    name = fields.Char(required=True)
    color =  fields.Integer()

    _name_unique = models.Constraint('unique(name)', "Property tag name already exists.")
