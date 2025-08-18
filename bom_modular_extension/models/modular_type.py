from odoo import fields, models


class modularType(models.Model):
    _name = "modular.type"
    _description = "Help to give modular type to product"

    name = fields.Char(string="Name", required=True)
