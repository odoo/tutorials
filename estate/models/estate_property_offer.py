from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffers(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ("cancelled", "Cancelled"),
        ],
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", required=True
    )
    property_id = fields.Many2one(
        comodel_name="estate.property",
        string="Property",
        required=True,
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be positive."),
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.validity:
                offer.date_deadline = fields.Date.add(
                    fields.Date.today(), days=offer.validity
                )
            else:
                offer.date_deadline = False

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - fields.Date.today()).days
            else:
                offer.validity = 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            price = vals.get("price", 0.0)
            if property_id:
                property_obj = self.env["estate.property"].browse(property_id)
                best_price = property_obj.best_offer or 0.0
                if price < best_price:
                    raise UserError(
                        "Offer price must be greater than or equal to the best offer price."
                    )
        records = super().create(vals_list)
        for record in records:
            if record.partner_id:
                record.property_id.state = "offer_received"
        return records

    @api.ondelete(at_uninstall=False)
    def _ondelete(self):
        for record in self:
            record.property_id.selling_price = 0.0

    def action_offer_tick(self):
        for record in self:
            if (
                float_compare(
                    record.property_id.expected_price * 0.9,
                    record.price,
                    precision_digits=2,
                )
                > 0
            ):
                raise ValidationError(
                    "The offer price must be at least 90% of the expected price."
                )
            accepted_offer = self.search(
                [
                    ("property_id", "=", record.property_id.id),
                    ("status", "=", "accepted"),
                ],
                limit=1,
            )
            if accepted_offer:
                raise UserError("The offer for this property is already accepted.")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"
        return True

    def action_offer_cross(self):
        for record in self:
            if record.status == "accepted":
                record.status = "refused"
                record.property_id.state = "offer_received"
                record.property_id.buyer_id = False
                record.property_id.selling_price = 0.0
            else:
                record.status = "refused"
        return True
