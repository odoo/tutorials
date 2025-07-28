from odoo import api, fields, models
from odoo.exceptions import UserError

class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offers"

    _order = "price desc"

    _sql_constraints = [
        ("check_price", "CHECK(price >0)", "The price should be stricly positive")
    ]

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date().today()
            record.date_deadline = fields.Date.add(date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date().today()
            record.validity = (record.date_deadline - date).days

    @api.model
    def create(self, vals):
        self.env["estate.property"].browse(vals.get("property_id")).state = "offer_received"
        if self.env["estate.property"].browse(vals.get("property_id")).best_price > vals.get("price"):
            raise UserError("The offer price cannot be less than current best")
        return super().create(vals)

    def action_accept(self):
        for record in self:
            if (
                record.property_id.state != "sold"
                or record.property_id.state != "cancelled"
                or record.property_id.state != "offer_accepted"
            ):
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            record.status = "refused"
