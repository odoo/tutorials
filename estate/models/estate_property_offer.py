from dateutil.relativedelta import *

from odoo import fields, models, api, exceptions, _
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "The offers of real estate properties"
    _order = "price desc"
    _sql_constraints = [
        (
            'check_price',
            'CHECK(price > 0)',
            'The price must be strictly positive.',
        )
    ]

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(
        string='Deadline', compute='_compute_deadline', inverse="_inverse_deadline"
    )

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = (
                record.create_date or fields.Date.today()
            ) + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    @api.model
    def create(self, vals):
        property = self.env['estate.property'].browse(vals['property_id'])
        if property.offer_ids:
            max_offer = max(property.offer_ids.mapped('price'))
            if float_compare(vals['price'], max_offer, precision_digits=2) == -1:
                raise exceptions.UserError(
                    "The offer must be higher than %.2f" % max_offer
                )
        property.state = 'offer-received'
        return super().create(vals)

    def action_set_status_accepted(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer-accepted'

    def action_set_status_refused(self):
        for record in self:
            record.status = 'refused'
