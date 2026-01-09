from dateutil.relativedelta import relativedelta
from odoo import api, fields, models

from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property offer'
    _order = 'price desc'

    price = fields.Float("Price")
    status = fields.Selection(
        copy=False,
        selection=[('accepted', "Accepted"), ('refused', "Refused")],
    )
    partner_id = fields.Many2one(
        'res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', store=True)

    # SQL Constraint
    _check_offer_price = models.Constraint(
        'CHECK(price > 0)', "The selling price must be  positive")

    # Compute Methods
    # Depends Decorator
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for record in self:
            start_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.validity = (record.date_deadline - start_date).days

    # Action Funcitons
    def action_accept(self):
        for record in self:
            if record.property_id.state != 'offer_accepted':
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer_ids = self.partner_id
                record.property_id.state = 'offer_accepted'
            else:
                raise UserError('One offer has already been accepted')

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            record.property_id.state = 'new'
            record.property_id.selling_price = '0'
            record.property_id.buyer_ids = None
