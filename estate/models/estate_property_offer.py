from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    validity = fields.Integer(default=7, string="Validity (days)")
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        string="Deadline",
    )
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The price of an offer must be strictly positive.'),
    ]

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = (
                offer.create_date + relativedelta(days=offer.validity)
                if type(offer.create_date) is datetime
                else fields.Date.context_today(self) + relativedelta(days=offer.validity)
            )

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_accept_offer(self):
        if any(offer.status == 'accepted' for offer in self.property_id.offer_ids):
            raise UserError('An offer is already accepted.')

        self.status = 'accepted'
        self.property_id.partner_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'

    def action_refuse_offer(self):
        self.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            max_offer = max((offer.price for offer in self.env['estate.property'].browse(vals['property_id']).offer_ids), default=0.0)
            if max_offer > vals['price']:
                raise UserError(f"The offer price must be at least {max_offer:,.2f}")

        offers = super().create(vals_list)

        for vals in vals_list:
            self.env['estate.property'].browse(vals['property_id']).state = 'offer_received'

        return offers
