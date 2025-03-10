from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers on Estate Listed"
    _order = "price desc"

    price = fields.Float(string="Offered Price", required=True)
    validity = fields.Integer(string="Validity(in days)", default=7)
    deadline = fields.Date(
        compute="_compute_deadline",
        inverse="_inverse_validity",
        store=True,
        default=lambda self: fields.Date.add(fields.Date.today(), days=7),
        copy=False,
    )
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True, ondelete="cascade")
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )
    _sql_constraints = [
        ("positive_offer_price", "CHECK(price>0)", "Offer Price should be positive.")
    ]

    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)
        for offer in offers:
            if offer.property_id.state == "new":
                offer.property_id.state = "offer_received"

        return offers

    @api.onchange("status")
    def change_of_status(self):
        for record in self:
            other_accepted_offers = record.property_id.offer_ids.filtered(
                lambda o: o.status == "accepted"
            )
            print("check", other_accepted_offers.partner_id.name)
            if other_accepted_offers.partner_id.name == record.partner_id.name:
                record.property_id.state = "offer_received"
                record.property_id.selling_price = 0
                record.property_id.buyer = False

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            create_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.deadline = fields.Date.add(create_date, days=record.validity)

    def _inverse_validity(self):
        for record in self:
            create_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            if record.deadline:
                record.validity = (record.deadline - create_date).days

    def action_set_accept_offer(self):
        for record in self:
            if record.property_id.state == "offer_accepted":
                raise UserError("You can only accept offer ones.")
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
            record.property_id.buyer = record.partner_id
            record.status = "accepted"
        return True

    def action_set_refuse_offer(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.selling_price = 0
                record.property_id.state = "offer_received"
                record.property_id.buyer = False

        record.status = "refused"
        return True
