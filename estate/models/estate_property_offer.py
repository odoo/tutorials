from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )
    validity = fields.Integer("Validity(Days)", default=7)

    date_deadline = fields.Date("Deadline Date", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "The expected price must be strictly positive.",
        ),
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property = self.env["estate.property"].browse(val["property_id"])
            max_offer_price = max(property.offer_ids.mapped("price"), default=0.0)
            if val["price"] < max_offer_price:
                raise UserError("The offer must be higher than an existing offer!")
            property.state = "offer received"
            return super().create(vals)

    def action_set_accepted(self):
        for record in self:
            if record.property_id.selling_price == 0.0:
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = "offer accepted"

                remaining_offers = record.property_id.offer_ids.filtered(
                    lambda offer: offer.id != record.id
                )
                remaining_offers.write({"status": "refused"})
            else:
                raise UserError("One offer is already accepted")
        return True

    def action_set_refused(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.selling_price = 0.0
                record.property_id.buyer_id = False
            record.status = "refused"
        return True
