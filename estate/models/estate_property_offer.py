from odoo import api, fields, models
from odoo.tools.date_utils import date
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        (
            "price",
            "CHECK(price > 0)",
            "The price must be strictly positive.",
        )
    ]

    price = fields.Float()
    status = fields.Selection(
        copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")]
    )
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        related="property_id.property_type_id",
        store=True,
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or date.today()
            record.date_deadline = fields.Datetime.add(
                create_date, days=record.validity
            )

    @api.model_create_multi
    def create(self, vals_list):
        all_offers = self.search([])
        for vals in vals_list:
            self.env["estate.property"].browse(
                vals["property_id"]
            ).state = "offer_received"
            if any(record.price > vals["price"] for record in all_offers):
                raise ValidationError(
                    "Cannot create an offer with a lower amount than an existing offer."
                )
        return super().create(vals_list)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        self.ensure_one()
        other_records = self.search(
            [("id", "!=", str(self.id)), ("property_id", "=", self.property_id.id)]
        )
        for rec in other_records:
            if rec.status == "accepted":
                raise UserError("Cannot have more than one accepted offer.")
        self.status = "accepted"
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = "offer_accepted"
        return True

    def action_refuse_offer(self):
        self.ensure_one()
        old_status = self.status
        self.status = "refused"
        if old_status == "accepted":
            self.property_id.buyer_id = ""
            self.property_id.selling_price = 0
            self.property_id.state = "offer_received"
        return True
