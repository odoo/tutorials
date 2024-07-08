from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Properties Tag defined"

    name = fields.Char(string="Name", required=True)
