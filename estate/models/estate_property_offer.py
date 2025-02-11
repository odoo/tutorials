from odoo import fields, models, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers for Real Estate App"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
        string="Status",
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price > 0)",
            "Offer Price for the property should be strictly positive",
        )
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + relativedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = datetime.today() + relativedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                delta = record.date_deadline - datetime.today().date()
                record.validity = delta.days

    def estate_property_offer_action_accept(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("Offer is already accepted")
            elif (
                record.property_id.best_offer >= record.property_id.expected_price * 0.9
            ):
                # accept the selected offer
                record.status = "accepted"
                record.property_id.status = "offer_accept"
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price

                # reject the other offers for same property
                other_offers = record.property_id.offer_ids.filtered(
                    lambda o: o.id != record.id
                )
                other_offers.write({"status": "refused"})
            else:
                raise ValidationError(
                    f"The selling price must be atleast 90% of expected price"
                )

    def estate_property_offer_action_refuse(self):
        for record in self:
            if record.status == "refused":
                raise UserError("Offer is already refused")
            else:
                # refuse the selected offer
                record.status = "refused"
                record.property_id.status = "offer_reject"
                record.property_id.buyer_id = False
                record.property_id.selling_price = False
