# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_estate_account = fields.Boolean(string="Enable Invoicing", config_parameter="estate.auction")
    module_estate_auction = fields.Boolean(string="Automated Auction", config_parameter="estate.auction")
