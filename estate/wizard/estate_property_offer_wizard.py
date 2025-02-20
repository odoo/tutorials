# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOfferWizard(models.TransientModel):
    _name = "estate.property.offer.wizard"
    _description = "Estate Property Offer Wizards"

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    price = fields.Float(string="Offer Price", required=True)

    def action_create_offer(self):
        if self.price <= 0:
            raise UserError(_("Offer price must be positive."))

        self.env['estate.property.offer'].create({
            'partner_id': self.partner_id.id,
            'property_id': self.property_id.id,
            'price': self.price,
        })

        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Success"),
                "message": _("Offer has been created successfully!"),
                "type": "success",
                "sticky": False,
                "next": {"type": "ir.actions.act_window_close"}
            }
        }
