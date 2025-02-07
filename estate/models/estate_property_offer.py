# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Contains offer made to properties"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ]
    )
    partner_id = fields.Many2one(
        string="Partner", comodel_name="res.partner", required=True
    )
    property_id = fields.Many2one(
        string="Property", comodel_name="estate.property", required=True
    )

    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )

    _sql_constraints = [('check_offer_price', 'CHECK(price > 0)', 'Offer price must be stictly positive')]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if not record.create_date:
                record.date_deadline = fields.Date.add(
                    fields.Date.today(), days=record.validity
                )
                continue

            if record.validity >= 0:
                record.date_deadline = fields.Date.add(
                    record.create_date, days=record.validity
                )
                continue

            record.date_deadline = fields.Date.subtract(
                record.create_date, days=record.validity
            )

    def _inverse_deadline(self):
        for record in self:
            if not record.create_date:
                record.validity = (record.date_deadline - fields.Date.today()).days
                continue

            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        if any([x.status == "accepted" for x in self.property_id.offer_ids]):
            raise UserError('An offer was already accepted')

        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = "offer_accepted"

    def action_refuse_offer(self):
        if self.status == "accepted":
            self.property_id.buyer_id = None
            self.property_id.selling_price = 0

        self.status = "refused"
