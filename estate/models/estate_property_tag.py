from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate properties tag"

    name = fields.Char('Tag', required=True)
