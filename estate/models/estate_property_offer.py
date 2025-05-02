from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "An offer price must be strictly positive",
        )
    ]
    _order = "price desc"

    price = fields.Float("Price", required=True)
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    create_date = fields.Datetime(
        string="Created Date", default=fields.Datetime.now, readonly=True
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
        help="Validity in days for the offer",
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = (
                    fields.Datetime.from_string(record.create_date)
                    + timedelta(days=record.validity)
                ).date()
            else:
                record.date_deadline = False

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = 0

    def action_accept(self):
        for record in self:
            if record.property_id:
                if (
                    record.status == "accepted"
                    or record.property_id.state == "offer_accepted"
                ):
                    raise UserError("The offer is already accepted!!!")
                else:
                    record.status = "accepted"
                    record.property_id.state = "offer_accepted"
                    record.property_id.buyer_id = record.partner_id
                    record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            if record.property_id:
                if record.status == "refused":
                    raise UserError("The offer is already refused!!!")
                else:
                    record.status = "refused"

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env["estate.property"].browse(vals["property_id"])
            if property_id.state == "sold":
                raise UserError("You cannot make an offer on a sold property")
            if property_id.state == "new":
                property_id.state = "offer_received"
            if property_id.offer_ids:
                if vals["price"] <= property_id.offer_ids[0].price:
                    raise UserError(
                        "The offer price must be higher than the existing price"
                    )
        return super().create(vals_list)
