from dateutil.relativedelta import relativedelta
from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Type Description"

    name = fields.Char(required=True)