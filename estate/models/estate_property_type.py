from odoo import models, fields


class EstatePropertytype(models.Model):

    _name = "estate.property.type"
    _description = "estate property type description"

    name = fields.Char('Name', required=True)
