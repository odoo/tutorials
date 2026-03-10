from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Monetary(
        currency_field="currency_id", required=True, string="Offer Price"
    )
    currency_id = fields.Many2one(
        "res.currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True, string="Property")
    status = fields.Selection(
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    date_deadline = fields.Date(
        string="Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    validity = fields.Integer(
        default=7,
        store=True,
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "Offer Price Must be in Positive",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.validity:
                create_date = (
                    fields.Date.to_date(record.create_date) or fields.Date.today()
                )
                record.date_deadline = fields.Date.add(
                    create_date, days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                create_date = (
                    fields.Date.to_date(record.create_date) or fields.Date.today()
                )
                record.validity = (record.date_deadline - create_date).days

    @api.onchange("date_deadline")
    def _onchange_validity(self):
        if self.date_deadline:
            create_date = fields.Date.to_date(self.create_date) or fields.Date.today()
            self.validity = (self.date_deadline - create_date).days

    @api.constrains("price")
    def _check_offer_price(self):
        for record in self:
            if (
                float_compare(
                    record.price,
                    record.property_id.expected_price * 0.9,
                    precision_rounding=record.currency_id.rounding,
                )
                == -1
            ):
                raise ValidationError(
                    _("offer price cannot be lower than 90% of the expected price.")
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            best_offer = self.env["estate.property.offer"].search(
                [("property_id", "=", vals["property_id"])], order="price desc", limit=1
            )
            if vals["price"] <= best_offer.price:
                raise ValidationError(_("new offer should be greater than best offer."))
        offers = super().create(vals_list)
        return offers

    def action_accept_offer(self):
        accepted_records = self.search_count(
            [
                ("property_id", "=", self.property_id.id),
                ("status", "=", "accepted"),
            ],
        )
        if accepted_records:
            raise UserError(_("cannot accept multiple offer"))
        else:
            self.status = "accepted"
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            self.property_id.state = "accepted"
            other_offers = self.search(
                [
                    ("property_id", "=", self.property_id.id),
                    ("status", "!=", "accepted"),
                ]
            )
            other_offers.write({"status": "refused"})
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True
