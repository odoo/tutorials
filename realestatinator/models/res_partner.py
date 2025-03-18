# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.osv import expression


class Partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

