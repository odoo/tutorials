from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _order = 'id desc'

    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the property, e.g., Bhat House"
    )

    postcode = fields.Char(
        string="Postcode",
        help="Postal code of the property"
    )

    description = fields.Text(
        string="Description",
        help="Detailed description of the property"
    )

    date_availability = fields.Date(
        string="Available Date",
        copy=False,
        default=fields.Date.today,
        help="Date when the property will be available for sale"
    )

    expected_price = fields.Float(
        string="Expected Price",
        required=True,
        help="Price at which the property is expected to be sold",
        index="btree"
    )

    selling_price = fields.Float(
        string="Selling Price",
        readonly=True,
        copy=False,
        help="The price at which the property is actually sold"
    )

    bedrooms = fields.Integer(
        string="No. of Bedrooms",
        default=2,
        help="Number of bedrooms in the property"
    )

    living_area = fields.Integer(
        string="Living Area",
        help="The total living area of the property in square meters"
    )

    facades = fields.Integer(
        string="Facades",
        help="Number of facades of the property"
    )

    garage = fields.Boolean(
        string="Has Garage?",
        help="Indicates whether the property has a garage"
    )

    garden = fields.Boolean(
        string="Has Garden?",
        help="Indicates whether the property has a garden"
    )

    garden_area = fields.Integer(
        string="Garden Area",
        help="The area of the garden in square meters"
    )

    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ],
        help="The orientation of the garden"
    )

    active = fields.Boolean(
        string="Active",
        default=True,
        help="Indicates whether the property is active and available for sale"
    )

    state = fields.Selection(
        string="Current State",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', 'Sold'),
            ('cancelled', "Cancelled")
        ],
        required=True,
        copy=False,
        default='new',
        help="The current state of the property"
    )

    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        string="Property Type",
        help="The type of the property (e.g., apartment, house, etc.)"
    )

    buyer = fields.Many2one(
        comodel_name='res.partner',
        string="Buyer",
        help="The buyer who purchased the property"
    )

    salesman = fields.Many2one(
        comodel_name='res.users',
        string="Salesman",
        default=lambda self: self.env.user,
        help="The salesperson responsible for the property"
    )

    tag_ids = fields.Many2many(
        comodel_name='estate.property.tags',
        string="Tags",
        required=True,
        help="Tags associated with the property (e.g., luxury, beachfront)"
    )

    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_id',
        help="Offers made for this property"
    )

    total_area = fields.Float(
        compute='_compute_total_area',
        help="The total area of the property (living area + garden area)"
    )

    best_price = fields.Float(
        compute='_compute_best_price',
        help="The best price offered for the property"
    )

    _sql_constraints = [
        (
            'check_expected_price',
            'CHECK(expected_price > 0)',
            "The Expected Price must be strictly positive"
        ),
        (
            'check_selling_price',
            'CHECK(selling_price > 0)',
            "The Selling Price must be strictly positive"
        )
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property_record in self:
            property_record.total_area = property_record.living_area + property_record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property_record in self:
            if property_record.offer_ids:
                property_record.best_price = max(property_record.offer_ids.mapped('price'))
            else:
                property_record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden_area_orientation(self):
        """Automatically set garden area and orientation if garden exists."""
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel_button(self):
        """Cancel the property sale."""
        if self.state == 'sold':
            raise UserError("Sold properties cannot be cancelled.")
        self.state = 'cancelled'

    def action_sold_button(self):
        """Mark the property as sold."""
        if self.state == 'cancelled':
            raise UserError("Cancelled properties cannot be sold.")
        self.state = 'sold'

    @api.constrains('selling_price', 'expected_price')
    def check_selling_price(self):
        """Ensure the selling price is at least 90% of the expected price."""
        for property_record in self:
            if (
                not float_is_zero(property_record.selling_price, precision_rounding=0.01)
                and float_compare(
                property_record.selling_price,
                property_record.expected_price * 0.9,
                precision_rounding=2
            )) == -1:
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    "You must reduce the expected price if you want to accept this offer."
                )
