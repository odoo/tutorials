from datetime import timedelta

from odoo import api, fields, models

from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(required=True)
    status = fields.Selection(
        [
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline"
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days

    def action_accept(self):
        for record in self:
            if record.property_id.state in ["cancelled", "sold"]:
                raise UserError("Cannot accept an offer for a cancelled or sold property")
            accepted_offers = record.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted"
            )
            if accepted_offers:
                raise UserError("an offer has already been accepted for this property")
            record.status="accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            if record.property_id.state in ["cancelled", "sold"]:
                raise UserError("Cannot modify offers for a sold or cancelled property")
            if record.status == "accepted":
                record.property_id.selling_price = 0.0
                record.property_id.buyer_id = False
                record.property_id.state = "new"
            record.status = "refused"
