from odoo import models, fields


class ResUsers(models.Model):
    _name = 'res.users'
    _inherit = ['res.users']

    building = fields.One2many("estate.building", "salesperson_id", string="Listings")
