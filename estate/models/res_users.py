from odoo import fields, models


class user(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", inverse_name="user_id", domain=[('state', 'in', ['new', 'offer_received'])])
