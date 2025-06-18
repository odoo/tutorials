from datetime import date, timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.deadline = date.today() + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.deadline:
                record.validity = (record.deadline - date.today()).days

    def offer_accept(self):
        if 'accepted' in self.mapped("property_id.offer_ids.status"):
            raise UserError("An offer is already accepted.")
        for record in self:
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

    def offer_refuse(self):
        for record in self:
            record.status = 'refused'
