from odoo import fields, models


class EstateType(models.Model):
    _name = "estate.property.type"
    _description = "Properties types of estate."

    name = fields.Char(string="Name", required=True)
