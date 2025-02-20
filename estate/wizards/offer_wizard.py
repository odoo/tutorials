# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class OfferWizard(models.TransientModel):
    _name = "offer.wizard"

    price = fields.Float(string="Price", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, ondelete='cascade')
    validity = fields.Integer(string="validity", default=7)
    date_deadline = fields.Date(string="valid till", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def confirm_offer(self):
        for offer in self.property_id.offer_ids:
            if offer.status == "accepted":
                raise UserError("After accepting one property you can't create another one!!!")
        self.env['estate.property.offer'].create(
            {
                "partner_id": self.partner_id.id,
                "validity": self.validity,
                "date_deadline": self.date_deadline,
                "price": self.price,
                "property_id": self.property_id.id,
                "property_type_id": self.property_type_id.id
            }
        )
