from odoo import fields, models, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offers"
    _order = "price desc"

    price = fields.Float()
    state = fields.Selection(
        selection=[
            ('Accepted', 'Accepted'),
            ('Refused', 'Refused'),
        ],
        string="Status"
    )
    partner_id = fields.Many2one('res.partner', required=True, ondelete="cascade")
    property_id = fields.Many2one('estate.property', required=True, ondelete="cascade")
    validity = fields.Integer(default=7)
    deadline_date = fields.Date(compute="_compute_validity", inverse="_inverse_validity")
    created_date = fields.Date(default=lambda self: datetime.today())
    accepted = fields.Boolean(default=False)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True, ondelete="cascade")
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'Offer price can not be less than or equal to zero')
    ]

    @api.depends()
    def _compute_validity(self):
        for record in self:
            if record.created_date:
                record.deadline_date = record.created_date+timedelta(days=record.validity)
            else:
                record.deadline_date = False

    def _inverse_validity(self):
        for record in self:
            if record.deadline_date and record.created_date:
                record.validity = (record.deadline_date-record.created_date).days
            else:
                record.validity = 0

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if (record.property_id):
            record.property_id.state = "offer_received"
        return record

    def action_accept(self):
        for record in self:
            if record.property_id.buyer:
               raise UserError("You can not accept offer it is already accepted")
            else:
                record.property_id.buyer = record.partner_id
                record.property_id.selling_price = record.price
                record.state = "Accepted"
                record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            if record.property_id.buyer == record.partner_id:
                record.property_id.buyer = None
                record.state = "Refused"
                record.property_id.state = "new"
            else:
                record.state = "Refused"
