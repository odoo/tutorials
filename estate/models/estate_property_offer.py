from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()

    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    _check_validity = models.Constraint(
        "CHECK(validity >= 0)", "Validity days cannot be negative!"
    )
    _check_price = models.Constraint(
        "CHECK(price > 0)", "An offer price must be strictly positive."
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            start_date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            offer.date_deadline = start_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                start_date = (
                    offer.create_date.date()
                    if offer.create_date
                    else fields.Date.today()
                )
                offer.validity = (offer.date_deadline - start_date).days

    @api.onchange("date_deadline")
    def _onchange_date_deadline(self):
        self._inverse_date_deadline()

    @api.model_create_multi
    def create(self, vals_list):
        temp_best_prices = {}

        for vals in vals_list:
            property_id = vals.get("property_id")
            price = vals.get("price", 0.0)
            if not property_id:
                continue
            property_rec = self.env["estate.property"].browse(property_id)
            current_best = temp_best_prices.get(property_id, property_rec.best_price)
            if float_compare(price, current_best, precision_rounding=0.01) <= 0:
                raise UserError(_("The offer must be higher than %s", current_best))
            temp_best_prices[property_id] = price

        offers = super().create(vals_list)

        properties_to_update = offers.mapped("property_id").filtered(
            lambda p: p.state == "new"
        )
        if properties_to_update:
            properties_to_update.write({"state": "offer_received"})

        return offers

    def action_accept(self):
        self.ensure_one()
        if "accepted" in self.property_id.offer_ids.mapped("status"):
            raise UserError(_("You cannot accept more than one offer."))
        self.status = "accepted"
        other_offers = self.property_id.offer_ids - self
        other_offers.write({"status": "rejected"})
        self.property_id.write(
            {
                "selling_price": self.price,
                "state": "pending_booking",
                "buyer_id": self.partner_id.id,
            }
        )

        seller_partner = self.property_id.salesperson_id.partner_id

        self.env["estate.booking"].create(
            {
                "property_id": self.property_id.id,
                "buyer_id": self.partner_id.id,
                "seller_id": seller_partner.id,
                "final_price": self.price,
            }
        )
        return True

    def action_reject(self):
        return self.write({"status": "rejected"})
