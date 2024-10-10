from odoo import fields,models




class PropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Real estate Tags"


    name = fields.Char(required=True)