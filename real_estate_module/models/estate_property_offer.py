from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError



class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Offers where one property can have multiple offers"
    _order = 'price desc'

    price = fields.Float(
        string="Offer Price",
        required=True,
        help="The price offered by the buyer for the property"
    )

    status = fields.Selection(
        selection=[
            ('accept', "Accepted"),
            ('reject', "Rejected")
        ],
        string="Status",
        copy=False,
        help="The current status of the offer"
    )

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Partner",
        required=True,
        help="The partner (buyer) who made the offer"
    )

    property_id = fields.Many2one(
        comodel_name='estate.property',
        string="Property",
        required=True,
        help="The property for which the offer is made"
    )

    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        string="Property Type",
        related='property_id.property_type_id',
        store=True
    )

    validity = fields.Integer(
        string="Validity (days)",
        default=7,
        help="Number of days the offer is valid"
    )

    date_deadline = fields.Date(
        string="Deadline Date",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True,
        help="The deadline for the offer, computed as creation date + validity days"
    )

    _sql_constraints = [
        (
            'check_offer_price',
            'CHECK(price > 0)',
            "The Offer Price must be strictly positive"
        )
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        """Computes date_deadline as create_date + validity days."""
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = False

    def _inverse_date_deadline(self):
        """Sets validity based on date_deadline - create_date."""
        for offer in self:
            if offer.date_deadline and offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validity = 7

    def action_confirm(self):
        """Accepts the offer and updates the property state."""
        
        for offer in self:
            if offer.property_id.state == 'sold':
                raise UserError("Cannot accept an offer for a sold property.")
            if offer.property_id.offer_ids.filtered(lambda o: o.status == 'accept'):
                raise UserError("Only one offer can be accepted per property.")
            offer.status = 'accept'
            offer.property_id.state = 'offer_accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price

    def action_reject(self):
        """Rejects the offer."""
        self.status = 'reject'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_obj = self.env['estate.property'].browse(vals.get('property_id'))

            if property_obj.best_price >= vals['price']:
                raise UserError("Offer Price is lower than the existing ones")

            property_obj.state = 'offer_received'

        return super().create(vals_list)
