from odoo import models, fields, api, exceptions
from datetime import timedelta


class Estatepropertyoffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer("Validity(7 Days)", default=7)
    date_deadline = fields.Date(
        "Deadline", compute="_compute_Validitydate", inverse="_inverse_datedeadline"
    )

    @api.depends("validity")
    def _compute_Validitydate(self):
        for record in self:
            current_date = fields.Date.today()
            record.date_deadline = current_date + timedelta(days=record.validity)

    def _inverse_datedeadline(self):
        for record in self:
            current_date = fields.Date.today()
            record.validity = (record.date_deadline - current_date).days

    def action_accept(self):
        if self.property_id.buyer_id:
            raise exceptions.UserError("This property already has a buyer!")
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.status = "accepted"

    def action_refuse(self):
        if self.status == "accepted":
            self.property_id.selling_price = 0
            self.property_id.buyer_id = ""
        self.status = "refused"
