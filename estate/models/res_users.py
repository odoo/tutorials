# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="seller_id", string="Properties", domain=[('state', 'in', ['new', 'offerreceived'])])
