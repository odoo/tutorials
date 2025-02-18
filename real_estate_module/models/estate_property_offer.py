from datetime import date, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    """Model representing property offers in the real estate module.
    
    Each property can have multiple offers, but only one can be accepted.
    Offers have a validity period and a deadline date.
    """
    _name = 'estate.property.offer'
    _description = "Property Offers where one property can have multiple offers"
    _order = 'price desc'  # Orders offers by price in descending order

    # Basic fields for offer details
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
    # Foreign keys linking to related models
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
        store=True,
        help="The type of the property linked to the offer"
    )
    # Validity and deadline fields
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
    # SQL constraint to ensure the price is strictly positive
    _sql_constraints = [
        (
            'check_offer_price',
            'CHECK(price > 0)',
            "The Offer Price must be strictly positive"
        )
    ]
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        """Compute the offer's deadline date as the creation date + validity days.
        
        If the offer has no creation date (e.g., a draft record), the deadline is not set.
        """
        for offer in self:
            if date.today():  # Ensure today's date is available
                offer.date_deadline = date.today() + timedelta(days=offer.validity)
            else:
                offer.date_deadline = False
    def _inverse_date_deadline(self):
        """Update the validity period based on the difference between deadline and creation date.
        
        If there is no valid deadline or creation date, reset the validity to 7 days.
        """
        for offer in self:
            if offer.date_deadline and offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validity = 7
    def action_confirm(self):
        """Accept an offer and update the property's state accordingly.
        
        - Ensures that only one offer can be accepted per property.
        - Updates the property's state, buyer, and selling price.
        """
        for offer in self:
            if offer.property_id.offer_ids.filtered(lambda o: o.status == 'accept'):
                raise UserError("Only one offer can be accepted per property.")
            offer.status = 'accept'
            offer.property_id.state = 'offer_accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
    def action_reject(self):
        """Reject an offer by setting its status to 'reject'."""
        self.status = 'reject'

    @api.model_create_multi
    def create(self, vals_list):
        """Override the create method to enforce offer price validation.
        
        - Ensures that the offer price is higher than any existing offers.
        - Updates the property's state to 'offer_received' upon a valid offer.
        """
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals.get('property_id'))
            if property.best_price >= vals['price']:
                raise UserError("Offer Price is lower than the existing ones")
            property.state = 'offer_received'
        return super().create(vals_list)
