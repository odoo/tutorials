from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta, datetime


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers of Estate Property"
    _order = "price desc"
    _sql_constraints = [
        ("_check_offer_price", "CHECK(price > 0)", "The Offer price must be positive.")
    ]

    price = fields.Float(string="Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False, string="Status"
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        "estate.property.types",
        related="property_id.property_type_id",
        string="Property Type",
        required=True,
    )
    validity = fields.Integer(default=7, string="Validity")
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", store=True, string="Deadline Date")

    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            property_id = val["property_id"]
            offer_price = val["price"]
            property = self.env["estate.property"].browse(property_id)
            is_state_new = (property.state == "new")
            result = self.read_group(
                domain=[("property_id", "=", property_id)],
                fields=["price:max"],
                groupby=[],
            )

            max_price = result[0]["price"] if result else 0

            if property.state == 'sold':
                raise ValidationError(_("Cannot create an offer on a sold property."))

            if max_price >= offer_price:
                raise UserError(_("You cannot create an offer with a lower or equal amount than an existing offer for this property."))

            if is_state_new:
                property.state = "offer_received"

        return super().create(vals)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            create_date = record.create_date or datetime.now()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            create_date = record.create_date or datetime.now()
            if record.date_deadline:
                delta = record.date_deadline - create_date.date()
                record.validity = delta.days

    def action_accept_offer(self):
        for record in self:
            existing = self.search(
                [
                    ("property_id", "=", record.property_id.id),
                    ("status", "=", "accepted"),
                ]
            )
            if existing:
                raise UserError(_("Another offer has been already accepted."))
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id.id

    def action_refuse_offer(self):
        for record in self:
            if record.status == "accepted":
                raise UserError(_("Accepted Offer cannot be Refused"))
            else:
                record.status = "refused"
