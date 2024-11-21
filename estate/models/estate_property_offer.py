from odoo import models, fields, api
from datetime import date, timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = 'price desc'
    _sql_constraints = [
        (
            'check_price_positive',
            'CHECK(price > 0)',
            "An offer price must be strictly positive.",
        )
    ]

    price = fields.Float("Price")
    status = fields.Selection(
        [('accepted', "Accepted"), ('refused', "Refused")], copy=False
    )
    partner_id = fields.Many2one('res.partner', "Partner", required=True)
    property_id = fields.Many2one('estate.property', "Property", required=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', store=True
    )

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            td = record.date_deadline - record.create_date.date()
            record.validity = td.days

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.selling_price = None
                record.property_id.buyer_id = None
            record.status = 'refused'

    def action_accept(self):
        for record in self:
            if record.property_id.selling_price:
                raise UserError(
                    self.env._("There is already an accepted offer for this property.")
                )
            else:
                record.status = 'accepted'
                record.property_id.state = 'accepted'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
