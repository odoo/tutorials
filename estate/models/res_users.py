from odoo import fields, models


class ResUsers(models.Model):
    _name = "res.users"
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson", string="Estate Properties", domain="[('state', 'in', ['new', 'received'])]")
