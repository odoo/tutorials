# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        selection=[
            ('accpeted', 'Accpeted'),
            ('refused', 'Refused'),
        ],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="validity", default=7)
    date_deadline = fields.Date(string="valid till", compute="_compute_date_deadline", inverse="_calculate_inverse_validity")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _calculate_inverse_validity(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def action_offer_accept(self):
        for record in self:
            if "accpeted" in record.property_id.offer_ids.mapped("status"):
                raise UserError("Offer is already accepted for this property")
            else :
                record.status = "accpeted"
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
        return True

    def action_offer_refuse(self):
        for record in self:
            if record.status == "accpeted":
                record.property_id.buyer_id = ""
                record.property_id.selling_price = 0.0
            record.status = "refused"
        return True

    _sql_constraints = [
        ('check_positive_value_offer_price', 'CHECK(price >= 0)',
         'Offer price must be positive')
    ]
