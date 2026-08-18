from odoo import models, fields, api
from datetime import timedelta

import logging

_logger = logging.getLogger(__name__)


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float("Offer Price")
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner = fields.Many2one(string="Buyer", comodel_name="res.partner", required=True)
    property = fields.Many2one(comodel_name="estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date("Offer Deadline", compute="_compute_deadline", inverse="_inverse_deadline")


    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            compare_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = compare_date + timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days
