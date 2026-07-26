from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class Offer(models.Model):
    _name = "estate_property_offer"
    _description = "Offer made to some estate (property)"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    property_id = fields.Many2one(
        string="Property",
        comodel_name="estate_property",
        required=True,
    )
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
    )
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_deadline",
        inverse="_inverse_deadline",
    )

    _positive_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "Offer price should be strictly positive",
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            curr_date = offer.create_date if offer.create_date else fields.Date.today()
            offer.date_deadline = curr_date + relativedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            date_diff = offer.date_deadline - (offer.create_date.date())
            offer.validity = date_diff.days

    def action_accept_offer(self):
        # check if there is no other accepted offers
        if "accepted" in self.property_id.offer_ids.mapped("status"):
            raise UserError("Only one offer can be accepted for a given property!")

        # update status, selling price, buyer
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id

    def action_refuse_offer(self):
        self.status = "refused"
        self.property_id.selling_price = 0
        self.property_id.buyer_id = None
