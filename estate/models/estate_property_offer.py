from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(required=True, string="Offer Price")
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True, string="Property")
    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[
            ("accepted", "Accepted"),
            ("refuse", "Refused"),
        ],
    )
    date_deadline = fields.Date(
        string="Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    validity = fields.Integer(
        string="Validity",
        default=7,
        store=True,
    )

    # alternative : create_date = record.create_date.date()
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.validity:
                create_date = (
                    fields.Date.to_date(record.create_date) or fields.Date.today()
                )
                record.date_deadline = fields.Date.add(
                    create_date, days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                create_date = (
                    fields.Date.to_date(record.create_date) or fields.Date.today()
                )
                record.validity = (record.date_deadline - create_date).days

    @api.onchange("date_deadline")
    def _onchange_validity(self):
        if self.date_deadline:
            create_date = fields.Date.to_date(self.create_date) or fields.Date.today()
            self.validity = (self.date_deadline - create_date).days

    def action_accept_offer(self):
        for record in self:
            if not (record.property_id.selling_price):
                record.property_id.selling_price = record.price
                record.status = "accepted"
                record.property_id.buyer_id = record.partner_id
            else:
                raise UserError("You cannot accept multiple offer")

    def action_refuse_offer(self):
        for record in self:
            record.status = "refuse"
        return True
