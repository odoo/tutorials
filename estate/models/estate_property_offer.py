from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price Offered")

    status = fields.Selection(
        [
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
        readonly=True,
    )

    partner_id = fields.Many2one(
        "res.partner",
        required=True,
        string="Buyer",
    )

    property_id = fields.Many2one(
        "estate.property",
        required=True,
        string="Property",
    )

    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
        string="Property Type",
    )

    validity = fields.Integer(
        default=7,
        string="Validity",
    )

    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = (
                record.create_date.date()
                if record.create_date
                else fields.Date.today()
            )
            record.validity = (record.date_deadline - create_date).days

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")

            if property_id:
                property_record = self.env["estate.property"].browse(property_id)

                if property_record.state in ["offer_accepted", "sold", "cancelled"]:
                    raise UserError(
                        "An offer cannot be created for this property."
                    )

                existing_offers = property_record.offer_ids

                if existing_offers:
                    max_price = max(existing_offers.mapped("price"))

                    if vals.get("price") <= max_price:
                        raise ValidationError(
                            f"The offer price must be higher than {max_price}."
                        )

        offers = super().create(vals_list)

        for offer in offers:
            if offer.property_id.state == "new":
                offer.property_id.state = "offer_received"

        return offers

    def accept_offer(self):
        for offer in self:
            offer.status = "accepted"

            offer.property_id.write(
                {
                    "selling_price": offer.price,
                    "buyer_id": offer.partner_id.id,
                    "state": "offer_accepted",
                }
            )

            remaining_offers = offer.property_id.offer_ids.filtered(
                lambda offer_: offer_.id != offer.id
            )

            remaining_offers.write({"status": "refused"})

    def reject_offer(self):
        for offer in self:
            offer.status = "refused"

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive.",
    )
