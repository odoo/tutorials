from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.estate_property_type_id",
        store=True,
    )

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)", "The offer price must be strictly positive."
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = (
                fields.Date.to_date(record.create_date) or fields.Date.today()
            )
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = (
                fields.Date.to_date(record.create_date) or fields.Date.today()
            )
            if record.date_deadline:
                record.validity = (record.date_deadline - create_date).days

    @api.model
    def create(self, vals_list):
        property_record = self.env["estate.property"].browse(
            vals_list[0]["property_id"]
        )
        if any(property_record.best_offer > vals["price"] for vals in vals_list):
            raise UserError(
                self.env._("You can't create an offer lower than the best offer.")
            )
        property_record.state = "offer_received"
        return super().create(vals_list)

    def action_confirm(self):
        for record in self:
            if record.status == "refused":
                raise UserError(self.env._("You can't accept an refused offer."))
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id.id
            record.property_id.state = "offer_accepted"
            for offer in record.property_id.offer_ids:
                if offer != record:
                    offer.status = "refused"
        return True

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                raise UserError(self.env._("You can't refuse an accepted offer."))
            record.status = "refused"
        return True
