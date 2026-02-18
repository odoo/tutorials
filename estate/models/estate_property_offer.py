from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"

    price = fields.Float(string="Offer Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("rejected", "Rejected")], copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (day)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    _check_price_positive = models.Constraint(
        "CHECK (price > 0)", "The property offer should be strictly positive"
    )

    def _get_create_date(self):
        self.ensure_one()
        return self.create_date.date() if self.create_date else fields.Date.today()

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            date = record._get_create_date()
            record.date_deadline = date + relativedelta(days=record.validity)

    @api.onchange("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                date = record._get_create_date()
                record.validity = (record.date_deadline - date).days

    def action_accept(self):
        for record in self:
            if record.property_id.offer_ids.filtered(lambda o: o.status == "accepted"):
                raise UserError("An offer has already been accepted for this property")

            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            record.status = "rejected"
        return True

    @api.constrains("price")
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.price, precision_digits=2):
                continue
            min_price = record.property_id.expected_price * 0.9
            if float_compare(record.price, min_price, precision_digits=2) == -1:
                raise ValidationError(
                    "The offer price can't be less than 90% of expected price"
                )
