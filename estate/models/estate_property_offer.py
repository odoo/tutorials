from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        required=True,
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
    )

    # Stat Button
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )

    # SQL Constraints
    sql_constraints = [
        ("check_offer_price", "CHECK(price>=0)", "The offer price must be positive.")
    ]

    @api.depends("validity")
    def _compute_date_deadline(self):
        for date in self:
            create_date = date.create_date or fields.Datetime.now()
            date.deadline = (
                fields.Datetime.from_string(create_date)
                + relativedelta(days=date.validity)
            ).date()

    def _inverse_date_deadline(self):
        for date in self:
            create_date = date.create_date or fields.Datetime.now()
            if date.deadline:
                delta = (
                    fields.Date.from_string(date.deadline)
                    - fields.Datetime.from_string(create_date).date()
                )
                date.validity = delta.days

    def action_accept(self):
        for record in self:
            other_accepted_offer = record.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted"
            )

        if other_accepted_offer:
            raise UserError(
                "Another offer has already been accepted for this property."
            )

        record.status = "accepted"
        record.property_id.state = "offer_accepted"
        record.property_id.buyer_id = record.partner_id
        record.property_id.selling_price = record.price
        return True

    def action_refused(self):
        for record in self:
            record.status = "refused"
            record.property_id.state = "offer_received"
            record.property_id.buyer_id = False
            record.property_id.selling_price = 0.0
        return True

    @api.constrains("price")
    def _check_selling_price(self):
        for record in self:
            if (
                float_compare(
                    record.price,
                    0.9 * record.property_id.expected_price,
                    precision_digits=2,
                )
                < 0
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price."
                )
        return True

    # CRUD Methods
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
