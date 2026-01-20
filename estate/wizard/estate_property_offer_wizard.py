# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "Estate Property Offer Wizard"

    price = fields.Float(string="Price", required=True)
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer",
                               required=True, default=lambda self: self.env.user)

    def submit_offer(self):
        active_property_id = self.env.context.get("active_ids")
        properties = self.env["estate.property"].browse(active_property_id)
        properties = list(filter(lambda x: x.state in (
            'new', 'offer_received'), properties))

        for property in properties:
            self.env["estate.property.offer"].create({
                'price': self.price,
                'partner_id': self.buyer_id.id,
                'property_id': property.id
            })

        return {"type": "ir.actions.act_window_close"}
