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
        for vals in vals_list:
            property = self.env["estate.property"].browse(vals.get("property_id"))

            if self.search(
                [("property_id", "=", property.id), ("price", ">=", vals.get("price"))]
            ):
                raise ValidationError("Can't make an offer lower than an existing one!")

            if property.state == "new":
                property.state = "offer_received"
        return super().create(vals_list)

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
        if self.property_id.state == "offer_accepted":
            raise UserError("You can only accept offer ones.")
        self.property_id.selling_price = self.price
        self.property_id.state = "offer_accepted"
        self.property_id.buyer = self.partner_id
        self.status = "accepted"

    def action_set_refuse_offer(self):
        if self.status == "accepted":
            self.property_id.selling_price = 0
            self.property_id.state = "offer_received"
            self.property_id.buyer = False

        self.status = "refused"
