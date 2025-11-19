# Python Imports
from datetime import timedelta

# Odoo Imports
from odoo import _, api, fields, models
from odoo.tools import float_compare
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offers'
    _order = 'price desc'

    # -----------------------------
    # SQL Constraints
    # -----------------------------
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'Offer price cannot be negative or zero.'),
    ]

    # -----------------------------
    # Field Declarations
    # -----------------------------
    price = fields.Float(string='Price', required=True, help='The offer price proposed by the partner.')
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False, help='Current status of the offer: Accepted or Refused.'
    )
    validity = fields.Integer(string='Validity (days)', default=7, help='Number of days this offer remains valid from the creation date.')
    date_deadline = fields.Date(
        string='Deadline', compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        help='Deadline date until which the offer is valid.'
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True, help='The partner who made this offer.')
    property_id = fields.Many2one('estate.property', string='Property', required=True, help='The property this offer is related to.')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True, help='Type of the related property.')

    # -----------------------------
    # Compute / Inverse Methods
    # -----------------------------
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        """
        Compute the deadline by adding the validity period (in days) to the creation date.
        Uses today's date if creation date is not available.
        Sets deadline to False if validity is not set.
        """
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.context_today(record)
            record.date_deadline = create_date + timedelta(days=record.validity) if record.validity else False

    def _inverse_date_deadline(self):
        """
        Recalculate the validity period based on the difference between the deadline
        and the creation date (or today's date if creation date is missing).
        Validity is set to zero if no deadline is specified.
        """
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.context_today(record)
            if record.date_deadline:
                delta = record.date_deadline - create_date
                record.validity = max(delta.days, 0)
            else:
                record.validity = 0

    # -----------------------------
    # CRUD Methods
    # -----------------------------
    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to validate offer before creation:
        - Ensure property and price are provided.
        - Prevent creating offers lower than existing offers.
        - Update property state if it's 'new'.
        """
        for vals in vals_list:
            property_id = vals.get('property_id')
            offer_price = vals.get('price', 0.0)
            if not property_id or not offer_price:
                raise UserError(_('Both property and price must be provided.'))

            Property = self.env['estate.property'].browse(property_id)

            for offer in Property.offer_ids:
                if float_compare(offer_price, offer.price, precision_rounding=0.01) < 0:
                    raise UserError(_('Cannot create an offer lower than an existing offer.'))

            if Property.state == 'new':
                Property.state = 'offer_received'

        # Pass all valid vals to super
        return super().create(vals_list)

    # -----------------------------
    # Action Methods
    # -----------------------------
    def action_confirm(self):
        """
        Confirm the offer:
        - Set offer status to 'accepted'.
        - Update related property status and selling details.
        """
        self.ensure_one()
        for record in self:
            record.status = 'accepted'
            record.property_id.write({
                'state': 'offer_accepted',
                'selling_price': record.price,
                'buyer_id': record.partner_id
            })

        (self.property_id.offer_ids - record).write({'status': 'refused'})

    def action_refuse(self):
        """
        Refuse the offer by setting its status to 'refused'.
        """
        self.ensure_one()
        for record in self:
            record.status = 'refused'
