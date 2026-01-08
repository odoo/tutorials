from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo import fields, models, api


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string="Price")
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string="Status",
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = (
                    offer.create_date.date()
                    + relativedelta(days=offer.validity)
                )
            else:
                offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                offer.validity = (
                    offer.date_deadline
                    - offer.create_date.date()
                ).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.buyer_id:
                raise UserError("Property already accepted")

            other_offer = offer.property_id.offer_ids - offer
            other_offer.write({'status': 'refused'})

            offer.status = "accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True

    _check_offer_price_positive = models.Constraint(
        'CHECK(price > 0)',
        'Offer price must be positive.',
    )
