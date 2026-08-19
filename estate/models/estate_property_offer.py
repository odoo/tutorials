from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    validity = fields.Integer("Validity (days)", default=7)

    # Many2one references
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    # Computed fields
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            base_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = base_date + timedelta(days=record.validity)

    @api.onchange("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            base_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            if record.date_deadline and base_date:
                record.validity = (record.date_deadline - base_date).days

    def action_confirm_offer(self):
        for offer in self:
            # Check property have already been sold or cancelled
            if offer.property_id.state in ["sold", "cancelled"]:
                raise UserError("This property has already been sold or cancelled!")

            # Any accepted offer?
            if any(o.status == "accepted" for o in offer.property_id.offer_ids):
                raise UserError("An offer have already been accepted!")

            # Accept offer
            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"
