from odoo import models, fields


class estate_tags(models.Model):
    _name = "estate.property.tags"
    _description = "This is Real Estate property tags"

    name = fields.Char(required=True)
