from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"
    _order = "price desc"

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('property_id') and vals.get('price'):
                property = self.env['estate.property'].browse(vals['property_id'])
                max_price = max((offer.price for offer in property.offer_ids), default=0.0)
                if vals['price'] < max_price:
                    raise UserError(_("The offer must be higher than %d.", max_price))
                if property.state == 'sold':
                    raise UserError(_("You cannot make an offer on a sold property."))
                if property.state == 'cancelled':
                    raise UserError(_("You cannot make an offer on a cancelled property."))
        return super().create(vals_list)

    price = fields.Float()
    status = fields.Selection([
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ], copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id")

    validity = fields.Integer(
        "Validity (days)",
        default=7,
        compute="_compute_validity",
        inverse="_compute_date_deadline",
    )
    date_deadline = fields.Date(
        "Deadline",
        compute="_compute_date_deadline",
        inverse="_compute_validity",
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.add((offer.create_date or fields.Date.today()), days=offer.validity)

    @api.depends('date_deadline')
    def _compute_validity(self):
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.to_date(offer.create_date or fields.Date.today())).days

    def action_accept_offer(self):
        for offer in self:
            offer.status = 'accepted'

            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id

            other_offers = offer.property_id.offer_ids - offer
            other_offers.action_refuse_offer()
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
        return True

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )
