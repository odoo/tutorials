from odoo import fields,models

class estate_property_tag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag file"

    name = fields.Char('Name',required=True)
    color = fields.Integer()
