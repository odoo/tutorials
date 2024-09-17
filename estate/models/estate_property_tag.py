from odoo import fields, models


class EstatePropertyTags(models.Model):
    _name = "estate.property.tag"
    _description = "Real estate property tag"

    name = fields.Char(required=True)
