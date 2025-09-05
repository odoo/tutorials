# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string='Offer Price')
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    created_date = fields.Date(default=fields.Date.context_today, string='Created Date')
    validity = fields.Integer(default=7, string='Validity (Days)')
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', string='Deadline Date', store='True')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('price', 'CHECK(price >= 0)', 'Offer price must be strictly positive')
    ]

    @api.depends('created_date', 'validity')
    def _compute_date_deadline(self):
        """
        Computes the deadline date for each offer record based on its creation date and validity period.

        If both 'created_date' and 'validity' are set, 'date_deadline' is calculated by adding the validity (in days)
        to the creation date. Otherwise, 'date_deadline' is set to False.

        This method is triggered automatically when either 'created_date' or 'validity' fields are changed.
        """

        for record in self:
            if record.created_date and record.validity:
                record.date_deadline = record.created_date + timedelta(days=record.validity)
            else:
                record.date_deadline = False

    def _inverse_date_deadline(self):
        """
        Inverse method for computing the 'validity' field based on 'date_deadline' and 'created_date'.

        This method updates the 'validity' field for each record by calculating the number of days
        between 'date_deadline' and 'created_date'. If either field is missing, 'validity' is set to 0.

        Used as an inverse function in computed fields to allow updating 'validity' when 'date_deadline' changes.
        """

        for record in self:
            if record.date_deadline and record.created_date:
                record.validity = (record.date_deadline - record.created_date).days
            else:
                record.validity = 0

    def offer_accepted_action(self):
        """
        Accepts an offer for a property, ensuring only one accepted offer per property.

        Iterates through each offer record, checks if there is already an accepted offer for the same property.
        If an accepted offer exists, raises a UserError to prevent multiple accepted offers.
        Otherwise, updates the property's selling price, buyer, and state to reflect the accepted offer,
        and sets the offer's status to 'accepted'.

        Raises:
            UserError: If the property already has an accepted offer.

        Returns:
            bool: True if the operation is successful.
        """

        for record in self:
            # breakpoint()
            existing_offer = self.search([('property_id', '=', record.property_id.id), ('status', '=', 'accepted')])
            if existing_offer:
                raise UserError('This property already has an accepted offer.')
            property_record = record.property_id
            property_record.selling_price = record.price
            property_record.buyer_id = record.partner_id
            record.status = 'accepted'
            property_record.state = 'offer_accepted'
        return True

    def offer_refused_action(self):
        """
        This action used to refuse an offer.

        Returns:
            bool: True when operation is successful.
        """
        for record in self:
            record.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals):
        """
        Creates new estate property offers and updates the related property's state and best price validation.

        For each offer in `vals`:
            - If the related property's state is `new`, it is updated to `offer_received`.
            - If the offer price is less than or equal to the property's best price, a UserError is raised.

        Args:
            vals (list of dict): List of values for new estate property offers.

        Returns:
            recordset: The newly created estate property offer records.

        Raises:
            UserError: If the offer price is not greater than the property's best price.
        """
        for record in vals:
            property_id = record['property_id']
            if property_id:
                property = self.env['estate.property'].browse(property_id)
                if property.state == 'new':
                    property.state = 'offer_received'
                if property and property.best_price:
                    if record['price'] <= property.best_price:
                        raise UserError('Offer price must be greater than best Offer Price')
        return super().create(vals)
