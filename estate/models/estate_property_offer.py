from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate property offer"
    _order = "price desc"

    price = fields.Float()
    state = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )

    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        "Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )

    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK (price > 0)",
            "The offer price should be positive.",
        )
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Datetime.add(
                record.create_date if record.create_date else fields.Datetime.today(),
                days=record.validity,
            )

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def action_refuse(self):
        for record in self:
            record.state = "refused"
            if record.property_id.state == "offer_accepted":
                record.property_id.state = "offer_received"
                record.property_id.selling_price = 0
                record.property_id.buyer_id = False
        return True

    def action_accept(self):
        self.ensure_one()
        if self.property_id.state in ["sold", "offer_accepted"]:
            raise UserError("This property has another accepted offer")
        self.state = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = "offer_accepted"
        for offer in self.property_id.offer_ids:
            if offer == self:
                continue
            offer.state = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if (
                float_compare(
                    vals["price"],
                    self.env["estate.property"].browse(vals["property_id"]).best_offer,
                    precision_rounding=self.env["estate.property"]
                    .browse(vals["property_id"])
                    .rounding,
                )
                < 0
            ):
                raise UserError("Cannot add an offer lower than the current best one.")
            self.env["estate.property"].browse(
                vals["property_id"]
            ).state = "offer_received"
        return super().create(vals_list)
