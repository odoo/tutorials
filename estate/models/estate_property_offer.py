# imports of python lib
from datetime import timedelta

# imports of odoo
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    # === Private attributes ===
    _name = 'estate.property.offer'
    _description = 'Offers for all the property listings.'
    _order = 'price desc'

    # SQL Constraints
    _sql_constraints = [
        ('check_price_positive', 'CHECK(price > 0)', 'Offer price must be strictly positive.'),
    ]

    # ------------------------
    # Fields declaration
    # -------------------------
    price = fields.Float(string='Price')
    validity = fields.Integer(default=7)

    # Selection fields
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        string='Status',
        copy=False
    )

    # Computed fields
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)

    # Many2one fields
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property Name', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    # --------------------
    # Compute methods
    # --------------------
    @api.depends('create_date', 'validity', 'date_deadline')
    def _compute_date_deadline(self):
        for offer in self:
            base_date = (offer.create_date or fields.Datetime.now()).date()
            offer.date_deadline = base_date + timedelta(days=offer.validity or 0)

    def _inverse_date_deadline(self):
        for offer in self:
            base_date = (offer.create_date or fields.Datetime.now()).date()
            if offer.date_deadline:
                offer.validity = (offer.date_deadline - base_date).days

    # ---------------------
    # CRUD methods
    # ---------------------
    @api.model_create_multi
    def create(self, vals_list):
        """Overrided the default create method to enforce business rules when creating an offer.

        Logic implemented:
        1. Checks if the offer amount is lower than existing offer for the property.
            - If so raises a UserError to prevent the creation of the offer.
        2. If the offer is valid, updates the related property's state to 'offer_received'.

        Args:
            vals (dict): The values used to create the new estate.property.offer record.

        Returns:
            recordset: the newly created estate.property.offer record.

        Raises:
            UserError: If the offer amount is lower than an existing offer for the property.
        """
        for vals in vals_list:
            property_id = vals.get('property_id')
            offer_price = vals.get('price', 0.0)
            if not property_id or not offer_price:
                raise UserError('Both Property and Price must be provided.')

            property_obj = self.env['estate.property'].browse(property_id)
            for offer in property_obj.offer_ids:
                if float_compare(offer_price, offer.price, precision_rounding=0.01) < 0:
                    raise UserError('You cannot create an offer with an amount lower than existing offer.')

            if property_obj.state == 'new':
                property_obj.state = 'offer_received'

        return super().create(vals_list)

    # -------------------
    # Action methods
    # -------------------
    def action_accept(self):
        """Accept the offer and update the related property accordingly.

        - Sets the offer's status to 'accepted'.
        - Sets all the offer's status to 'refused'.
        - Updates the property's selling price and buyer.
        - Updates the property's state to 'offer_accepted'.

        Raises:
            UserError: If the property is already marked as 'sold'.
        """
        for offer in self:
            if offer.property_id.state == 'sold':
                raise UserError('You cannot accept an offer for a sold property.')

            offer.status = 'accepted'
            (offer.property_id.offer_ids - offer).write({'status': 'refused'})
            property = offer.property_id
            property.write({
                'selling_price': offer.price,
                'buyer_id': offer.partner_id,
                'state': 'offer_accepted'
            })
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = 'refused'
        return True
