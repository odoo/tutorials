from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Show offer given by buyer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[("Accepted", "Accepted"), ("Refused", "Refused")],
        string="Status",
        copy=False,
    )

    partner_id = fields.Many2one("res.partner", required=True, string="Buyer")
    property_id = fields.Many2one(
        "estate.property", required=True
    )  # Many2one use for One2many

    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline Date",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() or fields.Date.today()
            record.validity = (
                (record.date_deadline - create_date).days if record.date_deadline else 0
            )

    def action_accepted(self):
        for record in self:
            record.status = "Accepted"

        if record.property_id.state == "offer_accepted":
            raise UserError("One Offer already Accepted, can'nt accept another offer")

        record.property_id.selling_price = record.price
        record.property_id.buyer_id = record.partner_id
        record.property_id.state = "offer_accepted"
        record.status = "Accepted"

    def action_refused(self):
        for record in self:
            if record.status == "Accepted":
                record.property_id.selling_price = 0.0
                record.property_id.buyer_id = False
                record.property_id.state = "new"
            record.status = "Refused"

    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price > 0)",
            "Offer Price must be strictly postitive",
        )
    ]

    @api.model
    def create(self, vals):
        property_id = vals.get("property_id")
        if property_id:
            property_record = self.env["estate.property"].browse(property_id)

            if property_record.state not in ["offer_accepted", "sold"]:
                property_record.state = "offer_received"

            existing_offer = self.env["estate.property.offer"].search(
                [("property_id", "=", property_id)], order="price desc", limit=1
            )

            if existing_offer and vals.get("price") <= existing_offer.price:
                raise ValidationError(
                    "Offer Price must be greater than the existing offer of %.2f."
                    % existing_offer.price
                )

        return super().create(vals)
