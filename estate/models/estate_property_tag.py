from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate properties tag declaration"

    name = fields.Char(string="Tag", required=True)
