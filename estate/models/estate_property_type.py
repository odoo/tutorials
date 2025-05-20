from dateutil.relativedelta import relativedelta
from odoo import fields, models


class EstateType(models.Model):
    _name = 'estate.property.type'
    _description = 'It allows to create a new property type'

    name = fields.Char(required=True)
