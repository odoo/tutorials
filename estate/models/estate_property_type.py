from odoo import fields, models


class EstatePropertyType(models.Model):
    name = fields.Char(required=True)
