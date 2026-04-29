from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Monetary(currency_field="currency_id")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        help="Status of the offer"
    )
    validity = fields.Integer(default=7, string="Validity (days)")

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", string="Property Type", store=True)

    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "the offer price must be strictly positive.",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.date_deadline = base_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()

            delta = record.date_deadline - base_date
            record.validity = delta.days

    @api.model
    def create(self, vals_list):

        for vals in vals_list:
            prop = self.env["estate.property"].browse(vals.get("property_id"))
            existing_prices = prop.offer_ids.mapped("price")

            if existing_prices and vals.get("price") < max(existing_prices):
                raise UserError(f"The offer must be higher than {max(existing_prices):.2f}")

            prop.state = "offer_received"

        return super().create(vals_list)

    def accept_offer(self):

        for record in self:

            if record.property_id.garden and record.property_id.garden_orientation == "south":
                if record.price < record.property_id.expected_price:
                    raise ValidationError("The offer is too low for a property with a garden in south orientation.")

            record.status = "accepted"
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

        return True

    def action_refuse(self):
        self.status = "refused"
        return True
