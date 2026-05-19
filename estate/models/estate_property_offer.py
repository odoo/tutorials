from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )
    property_type_id = fields.Many2one(
        string="Property Type",
        related="property_id.type_id",
        store=True,
    )

    _check_price = models.Constraint(
        "CHECK(price > 0)", "An offer price should be strictly positive."
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (
                fields.Date.to_date(record.create_date) or fields.Date.today()
            ) + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            delta = record.date_deadline - (
                fields.Date.to_date(record.create_date) or fields.Date.today()
            )
            record.validity = delta.days

    @api.model
    def create(self, vals_list):
        properties = self.env["estate.property"].browse(
            [vals["property_id"] for vals in vals_list]
        )
        properties_by_id = {prop.id: prop for prop in properties}
        for vals in vals_list:
            property = properties_by_id.get(vals["property_id"])
            best_price = property.best_price
            if property.state == "sold":
                raise UserError(_("You can't create an offer for a sold property."))
            if vals["price"] < best_price:
                raise UserError(
                    _(
                        "You can't create an offer with a lower amount than an existing offer."
                    )
                )
            property.state = "offer_received"
        return super().create(vals_list)

    def action_set_accepted(self):
        states = self.property_id.offer_ids.mapped("status")
        for record in self:
            if "accepted" in states:
                raise UserError(_("An offer has already been accepted."))
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
        return True

    def action_set_refused(self):
        for record in self:
            previous_status = record.status
            record.status = "refused"
            if previous_status == "accepted":
                record.property_id.buyer_id = None
                record.property_id.selling_price = 0
        return True
