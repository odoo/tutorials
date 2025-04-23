from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property tag for an estate"

    name = fields.Char("Name", required=True)
