import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "A property offer is an amount a potential buyer offers to the seller"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Deadline")
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True, string="Property type")
    active = fields.Boolean(default=True)

    _check_offer_price_positive = models.Constraint(
        'CHECK(price > 0)',
        'The offer price of a property cannot be negative',
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            creation_date = record.create_date or datetime.date.today()
            record.date_deadline = creation_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = record.date_deadline.day - record.create_date.day

    def action_accept_offer(self):
        for record in self:
            if 'accepted' in record.property_id.offer_ids.mapped("status"):
                raise UserError("Another offer has already been accepted for this property")
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
