from odoo import fields, models


class EstateProperties(models.Model):
    _name = "estate.property.types"
    _description = " Estate Property Types"

    name = fields.Char('Type', required=True)
