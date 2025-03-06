# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _inherit = 'estate.property.offer'

    sale_type = fields.Selection(related="property_id.sale_type", store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env["estate.property"].browse(vals["property_id"])
            expected_price = property_id.expected_price
            highest_offer = property_id.highest_offer
            if property_id.sale_type == 'auction':
                if vals['price'] < expected_price:
                    raise UserError(_(f"The offer must be higher than the expected price ({expected_price :.2f})."))
                temp_best_price = property_id.best_price
                property_id.sudo().write({'best_price': 0})
                new_offer = super().create(vals)
                property_id.sudo().write({'best_price': temp_best_price})
            else:
                new_offer = super().create(vals)
        return new_offer

    def write(self, vals):
        if 'price' in vals:
            for offer in self:
                expected_price = offer.property_id.expected_price
                if vals['price'] < expected_price:
                    raise UserError(_(f"The offer must be higher than the expected price ({expected_price:.2f})."))
        return super().write(vals)
