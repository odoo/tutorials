from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property.type'
    _description = "Real Estate Property Type"

    name=fields.Char(
        "Name",
        required=True,
    )
