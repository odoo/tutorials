from odoo import models, fields


class ResUserEstateProperty(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson_id", string="properties", domain=[('state', 'in', ['new', 'offer_received'])])
