from odoo import api, fields, models
from odoo.exceptions import UserError


class Offer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for a property of Estate"
    _order = "price desc"

    price = fields.Float(required=True)
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
        index=True,
        required=True,
    )
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline",
        inverse="_inverse_deadline",
    )
    property_type_id = fields.Many2one(related="property_id.type_id", store=True)

    _check_price_positive = models.Constraint(
        "CHECK(price > 0)",
        "The Price of an Offer should be positive.",
    )

    @api.depends("create_date", "create_date")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record_date = fields.Date.today()
            else:
                record_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(
                record_date,
                days=record.validity,
            )

    def _inverse_deadline(self):
        for record in self:
            record.validity = (
                record.date_deadline - fields.Date.to_date(record.create_date)
            ).days

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            record = self.env["estate.property"].browse(vals["property_id"])
            if record.state == "new":
                record.state = "offer_received"
            elif record.best_price > vals["price"]:
                raise UserError(self.env._("Offer cannot be lower than the best price"))
        return super().create(vals_list)

    def action_confirm_offer(self):
        for record in self:
            if "accepted" in record.property_id.offer_ids.mapped("status"):
                raise UserError(self.env._("Property already sold"))
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"
            record.property_id.partner_id = record.partner_id
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True
