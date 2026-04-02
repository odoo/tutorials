from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offers"

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + \
                    timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline -
                                   record.create_date.date()).days

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one(
        "res.partner",
        required=True
    )
    property_id = fields.Many2one(
        "estate.property",
        required=True
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline"
    )

    def action_confirm(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == "accepted":
                    raise UserError("Only one offer can be acceped....")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    def action_cancel(self):
        for record in self:
            if record.status == 'accepted':
                record.status = "refused"
                record.property_id.selling_price = False
                record.property_id.buyer_id = False
            else:
                record.status = 'refused'
