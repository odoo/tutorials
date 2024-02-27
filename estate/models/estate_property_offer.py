from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ('offer_price_stricly_positive', 'CHECK (price>0)', 'The offer price must be strictly positive.'),
    ]

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
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True, string="Property Type")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = fields.Date.add(date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    @api.model
    def create(self, vals):
        property_id = self.env['estate.property'].browse(vals.get('property_id'))
        if vals.get('price') <= property_id.best_price:
            raise UserError("The offer price should be higher than " + str(property_id.best_price))
        property_id.state = 'offer'
        return super().create(vals)

    def action_accept_offer(self):
        for offer in self:
            if offer.property_id.state in ('sold', 'canceled'):
                raise UserError("A sold/canceled property cannot accept an offer.")
            if offer.property_id.selling_price != 0.0:
                raise UserError("An offer already accepted for this property")
            offer.status = 'accepted'
            offer.property_id.state = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.partner_id = offer.partner_id
        return True

    def action_refuse_offer(self):
        self.status = 'refused'
        return True
