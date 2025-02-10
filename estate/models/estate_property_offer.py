from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property offers"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, ondelete='cascade')
    validity = fields.Integer("Validity (Days)", default=7)
    date_deadline = fields.Date(
        "Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )
    _sql_constraints = [
        ("offer_price_positive", "CHECK(price > 0)", "Offer price must be positive!")
    ]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.to_string(
                    fields.Date.from_string(record.create_date)
                    + timedelta(days=record.validity)
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    create_date = fields.Date.from_string(record.create_date)
                    deadline_date = fields.Date.from_string(record.date_deadline)
                    record.validity = (deadline_date - create_date).days
            else:
                record.validity = 7
    
    @api.model
    def create(self, vals):
        property_id = self.env["estate.property"].browse(vals.get("property_id"))
        if property_id.state == "new":
            property_id.state = "offer_received"
        else:
            max_offer = max(property_id.offer_ids.mapped("price"),default=0)
            if vals['price'] < max_offer:
                raise UserError('You cannot create an offer lower than an existing offer.')

        return super().create(vals)

    # action Methods
    def action_accept_offer(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("This offer has already been accepted.")

            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"
