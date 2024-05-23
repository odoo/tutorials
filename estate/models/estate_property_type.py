from odoo import fields, models
from datetime import date, datetime, time
from dateutil.relativedelta import relativedelta


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate property Type"
    name = fields.Char(required=True)