# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_estate_auction = fields.Boolean(
        string="Automate Auction",
        help="Automate Auction to Accept best offer at the end of Auction", default=False)
