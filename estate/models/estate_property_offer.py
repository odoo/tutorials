from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer for a property'
    _order = 'price desc'

    price = fields.Float("Price", required=True)
    status = fields.Selection(string="Status",
                              selection=[
                                  ("accepted", "Accepted"),
                                  ("refused", "Refused")
                              ],
                              copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse="_inverse_date_deadline")
    validity = fields.Integer(string="Validity", default=7)
    property_type_id = fields.Many2one(related='property_id.property_type_id', string="Property Type", store=True)

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price > 0)',
         'The price must be greater than 0.'),
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = offer.create_date or fields.Datetime.now() + timedelta(days=offer.validity)

    @api.model_create_multi
    def create(self, vals):
        offers = super().create(vals)
        for offer in offers:
            property = self.env['estate.property'].browse(offer.property_id.id)

            if property.state in ['offer_accepted', 'sold', 'cancelled']:
                raise UserError(_("You can make an offer on a property that new or hasn't accepted any offer yet!"))

            elif property.state == 'new':
                property.state = 'offer_received'

            highest_offer_price = max(
                property.offer_ids.filtered(lambda x: x.status != 'refused').mapped('price')) or -1
            if offer.price < highest_offer_price:
                raise UserError(_("You cannot make an offer lower than the best price."))
        return offers

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_accept_offer(self):
        if self.status:
            raise UserError(_("This offer is already accepted or refused."))
        self.status = "accepted"
        for offer in self:
            offer.property_id.accept_offer(offer)

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"
