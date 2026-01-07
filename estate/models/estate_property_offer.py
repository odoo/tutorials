from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ], copy=False, readonly=True)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_confirm(self):
        if self.property_id.selling_price or self.status == "accepted":
            raise UserError("Offer is already accepted")
        else:
            self.status = "accepted"
            self.property_id.buyer_id = self.partner_id
            self.property_id.selling_price = self.price

    def action_cancel(self):
        if self.status == "accepted":
            self.property_id.selling_price = False
        self.status = "rejected"
