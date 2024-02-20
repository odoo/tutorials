from odoo import models, fields, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Potential Buyer")
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _sql_constraints = [
        ('offer_price_stricly_positive', 'CHECK (price>0)', 'The offer price must be strictly positive.'),
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                create_date = fields.Date.from_string(offer.create_date)
                offer.date_deadline = fields.Date.add(create_date, days=offer.validity)
            else:
                offer.date_deadline = fields.Date.add(fields.Date.today(), days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:
                create_date = fields.Date.from_string(offer.create_date)
                offer.validity = (offer.date_deadline - create_date).days
            else:
                offer.validity = (offer.date_deadline - fields.Date.today()).days

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.state == 'sold' or offer.property_id.state == 'canceled':
                raise exceptions.UserError("A sold/canceled property cannot accept an offer.")
            if offer.property_id.selling_price != 0.0:
                raise exceptions.UserError("An offer already accepted for this property")
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.partner_id = offer.partner_id
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
        return True
