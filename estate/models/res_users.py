from datetime import datetime
from odoo import fields, models


class Resusers(models.Model):
    _inherit = "res.users"
    property_ids = fields.One2many(
        "estate.property",
        "sale_id",
        domain=lambda self: [("date_availability", "<=", datetime.now())],
    )
