from odoo import api, fields, models
from odoo.exceptions import UserError

from datetime import date, timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Estate Property offers"
    _order = "price desc"

 
    price = fields.Float('Price')


    status = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
            ('cancelled', 'Cancelled'),
        ],
        string="Status",
        copy=False,
        default='new'
    )

    active = fields.Boolean('Active', default=True)
   
    partner_id = fields.Many2one('res.partner', string="Partner",required=True)
    property_id = fields.Many2one('estate_property', string="Property",required=True)    
    # property_type_id = fields.Integer(related="property_id.property_type_id", required=True)

    property_type_id = fields.Many2one(
        comodel_name='estate_property_type',
        string='Property Type',
        related='property_id.property_type_id',
        store=True,
        readonly=True
    )


    validity = fields.Integer('Validity (in days)', default=7)

    create_date = fields.Datetime('Creation Date', readonly=True)

    date_deadline = fields.Date('Deadline', required=True, compute='_compute_date_deadline', store=True,inverse='_inverse_date_deadline')
    



    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        """Compute the deadline as create_date + validity days."""
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                # Fallback: If create_date is not set, use today's date
                record.date_deadline = date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        """Update validity when the deadline is changed."""
        for record in self:
            if record.date_deadline and record.create_date:
                delta = (record.date_deadline - record.create_date.date()).days
                record.validity = delta

    # _sql_constraints = [
    #     ('check_number_of_months', 'CHECK(number_of_months >= 0)', 'The number of months can\'t be negative.'),
    # ]
    
    def accept_offer(self):
        for offer in self:
            # Make sure only one offer is accepted per property
            property_obj = offer.property_id
            if property_obj:
                # Set the buyer and the selling price for the property
                property_obj.buyer_id = offer.partner_id
                property_obj.selling_price = offer.price
                # Change the status of the offer to accepted
                offer.status = 'accepted'

                # Set all other offers for this property to 'refused'
                other_offers = self.search([('property_id', '=', offer.property_id.id), ('id', '!=', offer.id)])
                other_offers.write({'status': 'refused'})

                # Change the status of the property to 'offer_accepted'
                property_obj.state = 'offer_accepted'

             

    def refuse_offer(self):
        for offer in self:
            offer.status = 'refused'


    
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to add custom business logic for offers in batch mode."""

        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])

            # Check if a higher or equal offer exists
            existing_offer = property_id.offer_ids.filtered(lambda offer: offer.price >= vals['price'])
            if existing_offer:
                raise UserError(
                    "Cannot create an offer with a lower or equal amount than an existing offer."
                )

            # Update the property state to 'Offer Received'
            property_id.state = 'offer_received'

        return super().create(vals_list)