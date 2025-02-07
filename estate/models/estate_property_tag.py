from odoo import fields,models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description ="It defines the estate property tags"

    name= fields.Char(required=True)
