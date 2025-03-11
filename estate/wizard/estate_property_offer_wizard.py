# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class EstatePropertyOfferWizard(models.Model):
    _name = "estate.property.offer.wizard"
    _description = "Estate Property Offer Wizard"

    property_ids = fields.Many2many('estate.property', string="Properties")
    buyer_id = fields.Many2one('res.partner', string="Buyer", required=True)
    price = fields.Float(string="Offer Price", required=True)
    validity = fields.Integer(string="Validity (Days)", default=7, required=True)

    def action_make_an_offer(self):
        offers = self.env["estate.property.offer"]
        for property in self.property_ids:
            offers.create({
                'property_id' : property.id,
                'partner_id': self.buyer_id.id,
                'price': self.price,
                'validity': self.validity,
            })
        return {'type': 'ir.actions.act_window_close'}
