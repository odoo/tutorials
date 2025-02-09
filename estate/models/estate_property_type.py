from odoo import models, fields


class EstateType(models.Model):
    _name = "estate.property.type"
    _description = "These are Estate Module Property Types"

    name = fields.Char(string="Name", required=True)
