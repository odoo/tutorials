from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real E-state offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string="Offer Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = fields.Date.add(base_date, days=record.validity)

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "An offer price must be strictly positive",
    )

    def _inverse_date_deadline(self):
        for record in self:
            base_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            if record.date_deadline:
                record.validity = (record.date_deadline - base_date).days

    def accept_button(self):
        for record in self:
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

    def reject_button(self):
        for record in self:
            record.status = "refused"
            if record.property_id.buyer_id == record.partner_id:
                record.property_id.buyer_id = False
                record.property_id.selling_price = False
                record.property_id.state = "offer_received"

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            property_record = self.env["estate.property"].browse(val.get("property_id"))
            property_record.state = "offer_received"
            if val.get("price", 0) < property_record.best_price:
                raise UserError(
                    f"The offer price must be higger than {property_record.best_price}."
                )

        return super().create(vals_list)
