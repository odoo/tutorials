from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float(required=True)
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property")

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline",
                                store=True)

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.'),
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 7

    def action_accept(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError("You cannot accept an offer for a sold property.")

            if record.property_id.buyer_id:
                raise UserError("Only one offer can be accepted per property.")

            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'


    def action_refuse(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError("You cannot refuse an offer for a sold property.")

            if record.status == 'accepted':
                record.property_id.buyer_id = False
                record.property_id.selling_price = 0

            record.status = 'refused'
