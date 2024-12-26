from odoo import api, models, fields
from datetime import timedelta, date
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
        string="Property Type",
    )

    _sql_constraints = [
        (
            "check_offer_price_positive",
            "CHECK(price > 0)",
            "The offer price must be strictly positive.",
        ),
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = (record.create_date + timedelta(days=record.validity)).date()
            else:
                record.date_deadline = date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for vals in vals_list:
            prop_id = vals["property_id"]
            offer_price = vals["price"]
            res = self.env["estate.property"].browse(prop_id)
            if prop_id:
                res.write({"state": "offer_received"})
                if offer_price:
                    existing_offers = self.search(
                        [("property_id", "=", prop_id), ("price", ">", offer_price)],
                        limit=1,
                    )
                    if existing_offers:
                        raise UserError(
                            "An offer with the higher price already exists."
                        )
        return records

    def action_offer_accepted(self):
        for record in self:
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

            for other_offer in record.property_id.offer_ids:
                if other_offer.id != record.id:
                    other_offer.status = "refused"
            return True

    def action_offer_refused(self):
        for record in self:
            record.status = "refused"
            return True
