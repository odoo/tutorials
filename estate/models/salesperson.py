from odoo import models, fields


class ResUsers(models.Model):
    _inherit = ["res.users"]

    building = fields.One2many("estate.buildings", "salesperson_id", string="Listings")
