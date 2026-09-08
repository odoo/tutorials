from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        'estate.property',
        "sales_person",
        string="Assigned Properties",
        domain=[("state", "in", ["new", "offer_received"])],
    )
    test = fields.Char()
