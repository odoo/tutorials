# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields
from odoo import models

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', 'salesman_id', domain="[('state', 'in', ['new','offer received'])]")
