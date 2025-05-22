from odoo import fields
from odoo import models


class ResUsers(models.Model):
    _inherit = 'res.users'

    # Relational
    estate_property_ids = fields.One2many('estate.property', 'salesperson_id', string="Estate properties", domain='[("state", "in", ["new", "recieved"])]')
