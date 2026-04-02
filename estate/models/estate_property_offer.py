from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")

    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
            ('pending', "Pending")
        ],
        string="Status",
        copy=False,
        default='pending',
    )

    partner_id = fields.Many2one('res.partner', required=True, string="Partner")
    property_id = fields.Many2one('estate.property', required=True, string="Property")

    validity = fields.Integer(string="Validity (days)", default=7, help='Number of days the offer is valid for')

    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", help="Deadline for the offer based on the validity period")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            start = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = start + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - start).days

    def action_accept(self):
        if self.property_id.state == 'sold':
            raise UserError(_("you cant accept a sold property"))
        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price

    def action_reject(self):
        if self.property_id.state == 'sold':
            raise UserError(_("You cant reject a sold property"))
        self.status = 'refused'
