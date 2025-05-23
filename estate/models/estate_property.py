from odoo import fields, models, api, tools
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "estate property description"
    name = fields.Char('Property Name', required=True)
    address = fields.Char('Property Address', required=True)
    postcode = fields.Char('Property Postcode', required=True)
    expected_price = fields.Float('Property Expected Price', digits=(16, 2), required=True)
    availability_date = fields.Date('Property Available', required=True, copy=False, default=lambda _: fields.Date.today() + relativedelta(months=3))
    furnished = fields.Boolean('Property Furnished', default=False)
    bedrooms = fields.Integer('Property Bedrooms', required=True, default=2)
    bathrooms = fields.Integer('Property Bathrooms', required=False, default=1)
    selling_price = fields.Float('Property Selling Price', digits=(16, 2), required=False, readonly=True, copy=False)
    living_area = fields.Integer('Property Living Area', required=False)
    garage = fields.Boolean('Property Has Garage', required=True)
    garden = fields.Boolean('Property Has Garden', required=True)
    garden_area = fields.Integer('Property Garden Area (sqm)', required=True)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="orientation of the garden")
    active = fields.Boolean('Property Active', default=True)
    state = fields.Selection(
        string='Property State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        default='new',
        required=True,
        copy=False
    )
    facades = fields.Integer('Property Facades')
    description = fields.Text('Property Description', default="No description provided.")

    # Many-To-One Relations
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', required=False)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesman_id = fields.Many2one('res.users', string='Salesman', required=True, default=lambda self: self.env.uid)

    # Many-To-Many Relations
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')

    # One-To-Many Relations
    offer_ids = fields.One2many('estate.property.offer', 'property_id')

    # Computed Fields
    total_area =fields.Integer('Property Total Area', compute='_calculate_total_area')
    best_price = fields.Float('Property Best Offer', digits=(16, 2), readonly=True, copy=False, compute='_get_best_price')

    # Ordering
    _order = "id desc"

    # DB Constraints
    _sql_constraints = [
        ("check_expected_price_is_positive", "CHECK(expected_price > 0)", "The expected price must be positive."),
        ("check_selling_price_is_positive", "CHECK(selling_price >= 0)", "The selling price must be positive."),
    ]

    # Python Constraints
    @api.constrains('selling_price')
    def _check_selling_price_not_lower_90p_expected_price(self):
        for property in self:
            if property.selling_price==0:
                continue
            comparing_result = tools.float_compare(property.selling_price, 0.9 * property.expected_price, precision_digits=6)
            if comparing_result < 0:
                raise ValidationError("Can't accept an offer with an amount less than 90% of the expected price.")

    @api.depends('offer_ids')
    def _get_best_price(self):
        _best_offer = 0
        for property in self:
            for offer in property.offer_ids:
                _best_offer = max(_best_offer, offer.price)
            property.best_price = _best_offer

    @api.depends('living_area', 'garden_area')
    def _calculate_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    # Actions
    def action_property_sold(self):
        for property in self:
            if property.state == 'cancelled':
                raise ValidationError("cancelled properties can't be set to `sold`.")
            if property.state != 'offer_accepted':
                raise ValidationError("You need to accept an offer for the property first.")
            for offer in property.offer_ids:
                if offer.status == 'accepted':
                    property.buyer_id = offer.partner_id
                    property.state = 'sold'
                    break
        return True

    def action_property_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise ValidationError("`sold` properties can't be cancelled.")
            property.state = 'cancelled'
        return True

    # Offers Interactions
    # Update Property Status based on offer creations/removals
    @api.onchange('offer_ids')
    def _update_property_state(self):
        if self.state in ('sold', 'cancelled'):
            return
        if self.state == 'new' and self.offer_ids:
            self.state = 'offer_received'
        if not self.offer_ids:
            self.state = 'new'

    def _make_effect(self, message):
        return {
            'effect': {
                'fadeout': 'fast',
                'message': message,
                'type': 'rainbow_man',
            }
        }

    def _notify_offer_received(self, offer):
        if self.state == 'new':
            self.state = 'offer_received'

    def _notify_offer_accepted(self, accepted_offer):
        if self.state == 'sold' or self.state == 'cancelled':
            return self._make_effect(f"The property is already {self.state}.")

        self.state = 'offer_accepted'
        self.selling_price = accepted_offer.price
        for offer in self.offer_ids:
            if offer.status == 'accepted':
                offer.status = 'refused'
        accepted_offer.status = 'accepted'
        return None

    def _notify_offer_refused(self, refused_offer):
        if self.state == 'sold' or self.state == 'cancelled':
            return self._make_effect(f"Warning: The property is already {self.state}.")
        refused_offer.status = 'refused'
        self.state = 'offer_received'
        self.selling_price = 0
        return None

    # CRUD overrides
    @api.ondelete(at_uninstall=False)
    def _unlink_except_new_cancelled(self):
        for property in self:
            if property.state not in ('new', 'cancelled'):
                raise ValidationError("You can't delete properties that are neither new nor cancelled.")

