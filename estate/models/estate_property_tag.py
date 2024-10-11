from odoo import fields, models 

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate_property_tag description"

    name = fields.Char(required=True)
    