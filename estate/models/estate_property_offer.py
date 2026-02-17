from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Esate Property Offer"

    price = fields.Float(string="Price Offered")
    status = fields.Selection(
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ("pending", "Pending"),
        ],
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Buyer")
    property_id = fields.Many2one("estate.property", required=True, string="Property")
    validity = fields.Integer(default=7, string="Validity")
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True
    )
    _check_offer_price = models.Constraint(
        "CHECK(price > 0)", "The offer price must be strictly positive."
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.validity = (record.date_deadline - create_date).days

    def accept_offer(self):
        for offer in self:
            if offer.property_id.state in ["sold", "cancelled"]:
                raise UserError(
                    "you cannot accpet an offer on a solid or cancelled property."
                )
            accepted_offer = offer.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted" and o != offer
            )
            if accepted_offer:
                raise UserError("only one offer can be accpeted for a property.")
            offer.status = "accepted"
            offer.property_id.write(
                {
                    "selling_price": offer.price,
                    "buyer_id": offer.partner_id.id,
                    "state": "offer_accepted",
                }
            )

    def reject_offer(self):
        for offer in self:
            property_rec = offer.property_id
            if property_rec.state in ["sold", "cancelled"]:
                raise UserError(
                    "you cannot refuse an offer on an sold or cancelled property."
                )
            if offer.status == "accepted":
                offer.status = "refused"
                property_rec.write(
                    {
                        "selling_price": 0.0,
                        "buyer_id": False,
                    }
                )
                other_pending = property_rec.offer_ids.filtered(
                    lambda o: o.status == "pending"
                )
                if other_pending:
                    property_rec.state = "offer_received"
                else:
                    property_rec.state = "new"
            else:
                offer.status = "refused"
