from odoo import fields, models


class inheritedUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate_classic.property", "salesman_id", domain="[('state', 'in', ['new', 'offer_received'])]")
