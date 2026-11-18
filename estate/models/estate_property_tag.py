from dateutil.relativedelta import relativedelta
from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Tag Description"

    name = fields.Char(required=True)
