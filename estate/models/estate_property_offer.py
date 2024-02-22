from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline"
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        string="Property Type",
        store=True
    )

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offer price must be positive.')
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = fields.Date.add(date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.buyer_id:
                raise UserError(
                    "This property already has an accepted offer."
                )
            offer.property_id.buyer_id = offer.partner_id.id
            offer.property_id.state = 'offer_accepted'
            offer.status = 'accepted'
            offer.property_id.selling_price = offer.price
        return True

    def action_refuse(self):
        for offer in self:
            if offer.status == 'accepted':
                raise UserError(
                    "You cannot refuse an accepted offer."
                )
            offer.status = 'refused'
        return True
