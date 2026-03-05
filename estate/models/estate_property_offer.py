from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer description"
    _order = "price desc"

    price = fields.Float(string="Price")
    property_offer_ids = fields.Integer(string="Offer")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
    )
    validity = fields.Integer(string="Validity(days)", default=7)
    date_deadline = fields.Date(
        compute="_compute_sum_date",
        inverse="_compute_validity",
        string="Deadline",
    )

    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        store=True,
        readonly=True,
    )

    @api.depends("validity")
    def _compute_sum_date(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "Offer Price field should always be positive",
    )

    def _compute_validity(self):
        for record in self:
            fields.Date.today() == record.date_deadline - timedelta(
                days=record.validity,
            )

    @api.onchange("date_deadline")
    def _onchange_validity(self):
        if self.date_deadline:
            create_date = fields.Date.to_date(self.create_date) or fields.Date.today()
            self.validity = (self.date_deadline - create_date).days

    @api.model
    def create(self, vals_list):

        for vals in vals_list:
            property_id = vals.get("property_id")
            price = vals.get("price")

            if property_id and price:
                property_rec = self.env["estate.property"].browse(property_id)

            if property_rec.best_price and price <= property_rec.best_price:
                raise UserError(
                    _("Offer price must be higher than the current best price."),
                )
            if property_rec.state == "new":
                property_rec.state = "offer_received"

        return super().create(vals_list)

    def action_accepted(self):
        accepted_records = self.search_count(
            [
                ("property_id", "=", self.property_id),
                ("status", "=", "accepted"),
            ],
            limit=1,
        )
        if accepted_records:
            raise UserError(_(" multiple offer can't be accepted"))

        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = "offer_accepted"
        other_offers = self.search(
            [
                ("property_id", "=", self.property_id),
                ("status", "!=", "accepted"),
            ],
        )
        other_offers.write({"status": "refused"})
        return True

    def action_refused(self):
        for record in self:
            record.status = "refused"
        return True
