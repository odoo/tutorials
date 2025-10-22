from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for the estate"

    name = fields.Char('Tag', required=True)
    description = fields.Char('Description')
