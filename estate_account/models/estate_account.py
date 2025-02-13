# -- coding: utf-8 --
# Part of Odoo. See LICENSE file for full copyright and licensing details. 

from odoo import models, fields

class AccountMove(models.Model):
    _inherit = "account.move"

    property_id = fields.Many2one("estate.property", string="Property", ondelete="cascade")
