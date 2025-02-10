# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api
from odoo import fields, models
from dateutil.relativedelta import relativedelta


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
    date_deadline = fields.Date(string="valid till", compute="_compute_date_deadline", inverse="_compute_inverse_validity")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _compute_inverse_validity(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days
