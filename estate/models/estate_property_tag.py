from odoo import fields, models

# estate.property.tag model 
class estatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag database table"

    name = fields.Char(string="Tag name", required=True)
    