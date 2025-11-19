from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate properties Types"

    name = fields.Char('Name', required=True, translate=True)
