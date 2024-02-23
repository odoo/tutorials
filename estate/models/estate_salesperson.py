from odoo import fields, models


class Salesperson(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        "estate.property",
        "salesman_id",
        domain=[('state', 'in', ['new', 'received'])])
