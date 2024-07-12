from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"
    _description = "For checking inheritance"

    property_ids = fields.One2many("estate.property", "sales_person", string="Properties", domain=[("state", "in", ["new", "offer received"])])
