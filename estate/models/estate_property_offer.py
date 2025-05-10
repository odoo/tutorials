from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "offer_price desc"

    offer_price = fields.Float(string="Price")
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one(
        "estate.property", string="Property", required=True, ondelete="cascade"
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Date Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    _sql_constraints = [
        (
            "check_offer_price_positive",
            "CHECK(offer_price > 0)",
            "The offer price must be strictly positive.",
        ),
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.context_today(record)
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            delta = record.date_deadline - create_date.date()
            record.validity = delta.days

    def action_accept(self):
        for offer in self:
            if offer.property_id.state in ["sold", "canceled"]:
                raise UserError(
                    "You cannot accept an offer for a sold or cancelled property."
                )
            if offer.property_id.offer_ids.filtered(lambda o: o.status == "accepted"):
                raise UserError("An offer has already been accepted for this property.")
            offer.status = "accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.offer_price
            offer.property_id.state = "offer_accepted"

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"

    # api.model_create_multi is used to create multiple records at once
    # self is the model class, not an instance of the model, Represents the model itself
    # vals_list is a list of dictionaries, each dictionary contains the values for a new record
    # self.env is the Odoo environment in which the model is being executed
    # self.env['estate.property'] is used to access the estate.property model
    # browse is used to fetch the specific property record, browse() doesn't immediately hit the database - it creates a recordset
    # super() calls the create method of the parent class (models.Model) to actually create the records in the database
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            new_price = vals.get("offer_price")
            property_id = vals.get("property_id")
            if property_id and new_price:
                property = self.env["estate.property"].browse(property_id)
                property.check_offer(new_price)
        return super().create(vals_list)
