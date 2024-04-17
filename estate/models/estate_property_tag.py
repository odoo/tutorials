from odoo import models,fields

class PropertyTag(models.Model):

    _name = "estate_property_tag"
    _description = "The tags that can be assigned to the property i.e. cozy, renovated, etc"
    name = fields.Char(required = True)