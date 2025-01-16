from odoo import fields, models
from dateutil.relativedelta import relativedelta


class Inherited_User(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property", "sales_person_id", string="property"
    )
