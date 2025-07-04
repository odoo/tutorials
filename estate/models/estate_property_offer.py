from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _sql_constraints = [
        (
            "estate_property_offer_price_positive",
            "CHECK(price > 0)",
            "The offer price must be strictly positive.",
        )
    ]

    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    create_date = fields.Datetime(
        string="Creation Date", readonly=True, default=fields.Datetime.now
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            creation_date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            if offer.validity:
                offer.date_deadline = creation_date + relativedelta(days=offer.validity)
            else:
                offer.date_deadline = creation_date

    def _inverse_date_deadline(self):
        for offer in self:
            creation_date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - creation_date).days
            else:
                offer.validity = 0

    def action_accept_offer(self):
        for record in self:
            record_property = record.property_id
            property_state = record_property.state

            if property_state == "offer_accepted":
                raise UserError("You can only accept one offer at a time.")
            if property_state == "sold":
                raise UserError("You cannot accept an offer on a sold property.")
            if property_state == "cancelled":
                raise UserError("You cannot accept an offer on a cancelled property.")

            other_offers = record_property.offer_ids.filtered(
                lambda o: o.id != record.id
            )
            other_offers.write({"status": "refused"})

            record.status = "accepted"
            record_property.write(
                {
                    "buyer_id": record.partner_id.id,
                    "selling_price": record.price,
                    "state": "offer_accepted",
                }
            )

        return True

    def action_refuse_offer(self):
        for record in self:
            record_property = record.property_id
            property_state = record_property.state

            if property_state in ["sold", "cancelled"]:
                raise UserError(
                    "You cannot refuse an offer on a sold or cancelled property."
                )
            if record.status == "accepted":
                raise UserError("You cannot refuse an already accepted offer.")

            record.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        estate_property_model_instance = self.env["estate.property"]
        for vals in vals_list:
            property_id = vals.get("property_id")
            estate_property = estate_property_model_instance.browse(property_id)
            best_price = estate_property.best_price
            if not estate_property:
                raise ValidationError("Property not found.")

            if estate_property.state in ["sold", "cancelled"]:
                raise ValidationError(
                    "You cannot create an offer for a sold or cancelled property."
                )

            if best_price >= vals.get("price", 0.0):
                raise ValidationError(
                    "The offer price must be strictly higher than the previous offers."
                )
            best_price = max(best_price, vals.get("price", 0.0))
            estate_property.state = "offer_received"

        return super().create(vals_list)
