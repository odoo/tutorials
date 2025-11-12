# -*- coding: utf-8 -*-

from odoo import api, exceptions, fields, models, _


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    estate_property_selling_way = fields.Selection(related='property_id.property_selling_way', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env["estate.property"].browse(vals["property_id"])
            expected_price = property_id.expected_price
            if property_id.property_selling_way == 'auction':
                if vals['price'] < expected_price:
                    raise exceptions.UserError((f"The offer must be bigger than expected price ({expected_price :.2f})."))
                temp_best_price = property_id.best_offer
                property_id.sudo().write({'best_offer': 0})
                new_offer = super().create(vals)
                property_id.sudo().write({'best_offer': temp_best_price})
            else:
                new_offer = super().create(vals)
        return new_offer

    def write(self, vals):
        if 'price' in vals:
            for offer in self:
                expected_price = offer.property_id.expected_price
                if vals['price'] < expected_price:
                    raise exceptions.UserError((f"The offer must be higher than the expected price ({expected_price:.2f})."))
        return super().write(vals)

    def action_accept(self, from_cron=False):
        for record in self:
            if record.estate_property_selling_way == "auction" and not from_cron:
                raise exceptions.UserError(_("You cannot accept offer manually while property is in auction"))
        return super().action_accept()

    def action_refuse(self, from_cron=False):
        for record in self:
            if record.estate_property_selling_way == "auction" and not from_cron:
                raise exceptions.UserError(_("You cannot refuse offer manually while property is in auction"))
        return super().action_refuse()
