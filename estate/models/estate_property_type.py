from odoo import models, fields


class Estate_Property_Type(models.Model):
    _name = "estate.property.type"

    name = fields.Char(required=True)
