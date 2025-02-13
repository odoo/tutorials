from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "All the available offer for the property"
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[("reject", "Reject"), ("accepted", "Accepted")],
    )
    validity = fields.Integer(string="Validity(days)", default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    buyer_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")
    property_type_id = fields.Many2one(
        "estate.property.types",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )

    _sql_constraints = [("check_offer_price", "CHECK(price > 0)", "Offer price must be stictly positive")]

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property = self.env["estate.property"].browse(val["property_id"])

            max_offer_price = max(property.offer_ids.mapped("price") or [0])
            if val.get("price", 0) <= max_offer_price:
                raise UserError(
                    "New offer should contain price higher than current one"
                )

            property.state = "offer_received"

        return super().create(vals)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = fields.Date.add(
                    record.create_date, days=record.validity
                )
            else:
                record.date_deadline = fields.Date.add(
                    fields.Date.today(), days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days

    def action_offer_accepted(self):
        for record in self:
            if record.status != "reject":
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.buyer_id
                record.property_id.state = "offer_accepted"
                other_offers = record.property_id.offer_ids.filtered(
                    lambda offer: offer.id != record.id
                )
                other_offers.write({"status": "reject"})

            else:
                raise UserError("One offer is already accepted")
        return True

    def action_offer_rejected(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.selling_price = 0
                record.property_id.buyer_id = False
            record.status = "reject"
        return True

