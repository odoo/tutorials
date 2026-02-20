from datetime import timedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True,
    )
    validity = fields.Integer(string="Validity")
    date_deadline = fields.Date(
        string='Date Deadline',
        default=fields.Date.context_today,
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )
    is_accepted = fields.Boolean(string="Accepted")
    is_refused = fields.Boolean(string="Refused")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for rec in self:
            if rec.create_date:
                rec.date_deadline = rec.create_date.date() + timedelta(days=rec.validity)
            else:
                rec.date_deadline = fields.Date.today() + timedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            if rec.create_date:
                rec.validity = (rec.date_deadline - rec.create_date.date()).days
            else:
                rec.validity = (rec.date_deadline - fields.Date.today()).days

    def accept(self):
        for rec in self:
            rec.status = "accepted"
            rec.is_accepted = True
            rec.is_refused = False

            rec.property_id.selling_price = rec.price
            rec.property_id.buyer_id = rec.partner_id

    def reject(self):
        for rec in self:
            rec.status = "refused"
            rec.is_accepted = False
            rec.is_refused = True

            rec.property_id.selling_price = 0
