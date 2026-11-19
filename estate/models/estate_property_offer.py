from odoo import api, models, fields
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = "id desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('refused', 'Refused'),
            ('accepted', 'Accepted'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (Days)")
    deadline = fields.Date(compute='_computed_date_deadline', inverse="_inverted_date_deadline")
    date = fields.Date(required=True, default=fields.Date.today(), string='Offer made on')
    property_type_id = fields.Many2one(related="property_id.type_id", stored=True)

    _strictly_positive_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be a positive value'
    )

    @api.depends('validity', 'create_date')
    def _computed_date_deadline(self):
        for offer in self:
            offer.deadline = fields.Date.add(offer.date, days=offer.validity)

    def _inverted_date_deadline(self):
        for offer in self:
            offer.validity = (offer.deadline - offer.date).days

    def accept_offer(self):
        for offer in self:
            if 'accepted' in offer.property_id.offer_ids.mapped('status'):
                raise UserError('An offer has already been accepted')
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
            offer.property_id.state = 'accepted'
            offer.property_id.partner_id = offer.partner_id
        return True

    def refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
            if (
                offer.property_id.state == 'accepted'
                and 'accepted' not in offer.property_id.offer_ids.mapped('status')
            ):
                offer.property_id.selling_price = 0.0
                offer.property_id.state = 'received'
                offer.property_id.partner_id = False
        return True
