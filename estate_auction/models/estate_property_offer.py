# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EstatePropertyOfferAuction(models.Model):
    _inherit = "estate.property.offer"

    is_auction = fields.Boolean(
        string="Is Auction",
        related="property_id.is_auction",
        store=True
    )

    @api.model_create_multi
    def create(self, vals_list):
        offers = super(EstatePropertyOfferAuction, self).create(vals_list)

        for offer in offers:
            offer.property_id._compute_highest_offer()

        return offers
    