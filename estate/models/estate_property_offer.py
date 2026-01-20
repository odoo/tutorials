from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("rejected", "Rejected"),
        ],
        copy=False,
        readonly=True,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "Offer price must be positive",
    )

    @api.model
    def create(self, vals):
        for val in vals:
            property_id = val.get("property_id")
            price = val.get("price")
            if property_id and price:
                property_rec = self.env["estate.property"].browse(property_id)
                if property_rec.offer_ids:
                    if price < property_rec.best_price:
                        raise UserError(
                            "The offer must be higher than existing offers."
                        )
        offer = super().create(vals)
        if offer.property_id and offer.property_id.state == "new":
            offer.property_id.state = "offer_received"
        return offer

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + relativedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = fields.Date.today() + relativedelta(
                    days=record.validity
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_if_delete_offer(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("You can not delete a property with accepted offer")

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days

    def action_accepted(self):
        for record in self:
            if record.property_id.selling_price or record.status == "accepted":
                raise UserError("Offer is already accepted")
            record.status = "accepted"
            rejected_offers = record.property_id.offer_ids.filtered(
                lambda offer: offer.id != record.id
            )
            for ro in rejected_offers:
                ro.status = "rejected"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

    def action_rejected(self):
        self.ensure_one()
        if self.status == "accepted":
            self.property_id.selling_price = False
        self.status = "rejected"
