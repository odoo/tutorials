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

    def action_btn_accepted(self):
        for record in self:
            if record.status == "refused":
                raise UserError(_("Offer is already refused"))
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_btn_refused(self):
        for record in self:
            if record.status == "accepted":
                raise UserError(_("Sorry offer sold out."))
            record.status = "refused"
            record.property_id.selling_price = 0
            record.property_id.buyer_id = ""
        return True

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

    def _compute_validity(self):
        for record in self:
            fields.Date.today() == record.date_deadline - timedelta(
                days=record.validity,
            )

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "Offer Price field should always be positive",
    )

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
