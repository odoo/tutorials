from odoo import models, fields, api, exceptions


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for Properties in the Estate app."

    _sql_constraints = [
        (
            "positive_offer_price",
            "CHECK(price>0)",
            "The offer price should be strictly positive.",
        )
    ]
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Datetime(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Datetime.add(
                record.create_date or fields.Datetime.today(), days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (
                record.date_deadline - (record.create_date or fields.Datetime.today())
            ).days

    def accept_offer_button_action(self):
        for record in self:
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

    def refuse_offer_button_action(self):
        for record in self:
            record.status = "refused"

    @api.model_create_multi
    def create(self, vals_dict):
        for vals in vals_dict:
            if (
                self.env["estate.property"].browse(vals["property_id"]).best_price
                > vals["price"]
            ):
                raise exceptions.UserError(
                    "Cannot add offer for a lower amount than already proposed."
                )
            self.env["estate.property"].browse(
                vals["property_id"]
            ).state = "offer_received"

        return super().create(vals_dict)
