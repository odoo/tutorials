from datetime import timedelta
from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = "Real estate property tag module"

    name = fields.Char(string="Name", required=True)
