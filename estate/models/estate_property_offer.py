from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
        help="Validity of the offer in days, after that it will be refused automatically.",
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            base_date = (
                fields.Date.to_date(offer.create_date)
                if offer.create_date
                else fields.Date.context_today(offer)
            )
            offer.date_deadline = base_date + timedelta(days=offer.validity or 0)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                base_date = (
                    fields.Date.to_date(offer.create_date)
                    if offer.create_date
                    else fields.Date.context_today(offer)
                )
                offer.validity = (offer.date_deadline - base_date).days
            else:
                offer.validity = 0

    # @api.onchange("date_deadline")
    # def _onchange_date_deadline(self):
    #     for offer in self:
    #         if offer.date_deadline:
    #             base_date = fields.Date.to_date(offer.create_date) if offer.create_date else fields.Date.context_today(offer)
    #             offer.validity = (offer.date_deadline - base_date).days
    #         else:
    #             offer.validity = 0

    def action_set_accepted(self):
        for offer in self:
            if offer.property_id.selling_price == 0.0:
                offer.status = "accepted"
                offer.property_id.state = "offer accepted"
                offer.property_id.selling_price = offer.price
                offer.property_id.buyer_id = offer.partner_id

                other_offers = offer.property_id.offer_ids - offer

                other_offers.write({"status": "refused"})
            else:
                raise UserError("One offer is already accepted for this property.")

    def action_set_refused(self):
        for offer in self:
            if offer.status == "accepted":
                offer.status = "refused"
                offer.property_id.state = "offer received"
                offer.property_id.buyer_id = False
                offer.property_id.selling_price = 0.0
            else:
                raise UserError("This offer is not accepted, so it cannot be refused.")

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be greater than 0."),
    ]
