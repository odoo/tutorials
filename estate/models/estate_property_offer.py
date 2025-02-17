from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import timedelta


class EstatePropertyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "The estate property offers model"
    _order = "price desc"

    price = fields.Float(string="Offer Price", required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    # property_state = fields.Selection(
    #     related="property_id.state", string="property state", store=True
    # )

    _sql_constraints = [
        (
            "check_offer_price",
            "CHECK(price>0)",
            "The offer price must be strictly positive",
        )
    ]
    validity = fields.Integer(string="Validity(days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_obj = self.env["estate.property"].browse(vals["property_id"])
            if property_obj.state=='sold':
                raise UserError("can not create offers for sold property")
            property_obj.state = "offer_received"
            if vals["price"] < property_obj.best_offer:
                raise UserError(
                    f"The offer must be higher than {property_obj.best_offer}"
                )
        return super().create(vals_list)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() or fields.Date.today()
            record.validity = (record.date_deadline - create_date).days

    def accept_offer(self):
        for record in self:
            if record.property_id.state == "sold":
                raise UserError("can not create offers for sold property")
            if record.property_id.selling_price:
                raise UserError("Offer already accepted")
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            for data in record.property_id.offer_ids:
                if data.status != "accepted":
                    data.status = "refused"

    def refused_offer(self):
        for record in self:
            record.status = "refused"
