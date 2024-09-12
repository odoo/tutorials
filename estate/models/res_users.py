from odoo import models, fields
from datetime import datetime


class Resusers(models.Model):
    _inherit = "res.users"
    property_ids = fields.One2many(
        "estate.property",
        "salesperson_id",
        domain=lambda self: [("date_availability", "<=", datetime.now())],
    )
