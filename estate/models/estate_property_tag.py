from odoo import fields, models


class EstateProperties(models.Model):
    _name = "estate.property.tag"
    _description = " Estate Property Tags"

    name = fields.Char('Name', required=True)
