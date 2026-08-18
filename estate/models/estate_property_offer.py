from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float('Price', required=True)
    property_id = fields.Many2one('estate.property', 'property_id', required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ]
    )
    # Pretty sure I shouldn't be doing this but I couldn't find another way
    property_state = fields.Selection(related="property_id.state")

    validity = fields.Integer(
        "Validity (days)",
        default=7,
        required=True,
    )
    date_deadline = fields.Date(
        "Deadline",
        required=True,
        compute="_compute_deadline",
        inverse="_inverse_deadline"
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            delta = offer.date_deadline - fields.Date.today()
            offer.validity = delta.days

    def action_offer_accept(self):
        for offer in self: 
            if offer.property_state in ('offer_accepted', 'sold', 'cancelled'):
                raise UserError("You can not accept more offers for this property")

            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
        
        return True

    def action_offer_refuse(self):
        for offer in self:
            offer.status = "refused"

        return True
