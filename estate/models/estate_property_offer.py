from dateutil.relativedelta import relativedelta
from odoo import api, models, fields
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The offer price must be strictly positive")
    ]
    _order = "price desc"

    price = fields.Float('price')
    status = fields.Selection(
        string='status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = start_date + \
                relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - start_date).days

    def action_accept(self):
        for record in self:
            if record.property_id.buyer_id:
                raise UserError("You already accepted an offer")
            if record.status == "refused":
                raise UserError("You already refused this offer")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("You already accepted this offer")
            record.status = "refused"
