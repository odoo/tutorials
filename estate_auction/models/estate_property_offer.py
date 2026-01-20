# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _inherit = ['estate.property.offer']

    sale_type = fields.Selection(related="property_id.sale_type", string="Sale Type")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            if property_id.expected_price > vals['price']:
                raise UserError("Offer Price should be greater than expected price.")
        return super().create(vals_list)
        