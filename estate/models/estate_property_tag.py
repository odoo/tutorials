from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tags model"

    name = fields.Char("Name", required=True)
