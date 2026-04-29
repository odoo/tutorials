from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _check_price = models.Constraint(
        'CHECK(price > 0.00)',
        "The offer's amount should be strictly positive.",
    )

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one("estate.property.type", store=True, related="property_id.property_type_id")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            date = datetime.today() if not record.create_date else record.create_date.date()
            record.date_deadline = date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            date = datetime.today() if not record.create_date else record.create_date.date()
            record.validity = (record.date_deadline - date).days

    @api.model
    def create(self, vals_list):
        for vals_dict in vals_list:
            property_id = self.env["estate.property"].browse(vals_dict["property_id"])
            offers = property_id.offer_ids
            if (len(offers) > 0 and vals_dict["price"] < min(offers.mapped("price"))):
                raise UserError("Offer with a lower value than an existing offer cannot be created.")
        return super().create(vals_list)

    def action_accept_offer(self):
        for record in self:
            if "accepted" in record.mapped("property_id.offer_ids.status"):
                raise UserError("Only one offer can be accepted")
            if (record.property_id.garden_orientation == "south" and
            float_compare(record.property_id.expected_price, record.price, 2) == 1):
                raise ValidationError("For properties with South oriented gardens, only offers having a price higher than the expected value of the property can be accepted")
        return self.status.write({
            "status": "accepted",
        }) and self.property_id.write({
            "state": "offer_accepted",
            "selling_price": record.price,
            "buyer_id": record.partner_id,
        })

    def action_refuse_offer(self):
        return self.write({
            "status": "refused",
        })
