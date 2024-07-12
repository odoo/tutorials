from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
    )
    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True, copy=False
    )
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(
        "Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )

    _sql_constraints = [
        ("check_offer_price", "CHECK(price > 0)", "The offer price must be positive"),
    ]

    @api.depends("validity", "date_deadline")
    def _compute_date_deadline(self):
        for record in self:
            current_date = fields.Date.today()
            record.date_deadline = current_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            current_date = fields.Date.today()
            record.validity = relativedelta(record.date_deadline, current_date).days

    def action_confirm(self):
        if self.property_id.buyer_id:
            raise UserError("Accepetd properties cannot be Accepetd.")
        else:
            self.status = "accepted"
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id

    def action_cancel(self):
        if self.status == "accepted":
            self.property_id.selling_price = 0.0
            self.property_id.buyer_id = ""
        self.status = "refused"

    @api.model
    def create(self, vals):
        estate_property = self.env["estate.property"].browse(vals["property_id"])
        if max(estate_property.offer_ids.mapped("price"), default=0) >= vals["price"]:
            raise UserError("offer with a lower amount than an existing offer")
        estate_property.state = "offer_received"
        return super().create(vals)
