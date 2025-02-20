from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
from datetime import date, timedelta

class EstateProperty(models.Model):
    """Model representing real estate properties available for sale."""

    _name = 'estate.property'
    _description = "Real Estate Property"
    _order = 'id desc'  # Sort properties by latest created ID
    _inherit = ['mail.thread','mail.activity.mixin']

    # Basic Property Details
    name = fields.Char(
        string="Name",
        required=True,
        help="Name of the property, e.g., 'Bhat House'"
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
    date_deadline = fields.Date(
        string="Date Deadline",
        copy=False,
        default=lambda self: fields.Date.today()+timedelta(days=10),
        help="Date when the property will not be available"
    )
    # Pricing Fields
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
    # Property Features
    bedrooms = fields.Integer(
        string="No. of Bedrooms",
        default=2,
        help="Number of bedrooms in the property"
    )
    living_area = fields.Integer(
        string="Living Area (sq.m)",
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
        string="Garden Area (sq.m)",
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
    # Property Status
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
            ('sold', "Sold"),
            ('cancelled', "Cancelled")
        ],
        required=True,
        copy=False,
        default='new',
        help="The current state of the property"
    )
    # Relationships
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        string="Property Type",
        help="The type of the property (e.g., Apartment, House, etc.)"
    )
    _is_commercial = fields.Boolean(
        compute='_compute_is_commercial',
        store=True
    )
    buyer_id = fields.Many2one(
        comodel_name='res.partner',
        string="Buyer",
        help="The buyer who purchased the property",
        domain="[('is_company','=',_is_commercial)]",
    )
    salesman_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesman",
        default=lambda self: self.env.user,
        help="The salesperson responsible for the property"
    )
    tag_ids = fields.Many2many(
        comodel_name='estate.property.tags',
        string="Tags",
        help="Tags associated with the property (e.g., Luxury, Beachfront)"
    )
    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_id',
        string="Offers",
        help="Offers made for this property"
    )
    # Computed Fields
    total_area = fields.Float(
        string="Total Area (sq.m)",
        compute='_compute_total_area',
        help="The total area of the property (living area + garden area)"
    )
    best_price = fields.Float(
        string="Best Offer Price",
        compute='_compute_best_price',
        help="The highest offer price received for the property"
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string="Company",
        default=lambda self: self.env.company
    )
    # SQL Constraints
    _sql_constraints = [
        (
            'check_expected_price',
            'CHECK(expected_price > 0)',
            "The Expected Price must be strictly positive."
        ),
        (
            'check_selling_price',
            'CHECK(selling_price > 0)',
            "The Selling Price must be strictly positive."
        )
    ]

    @api.depends('property_type_id')
    def _compute_is_commercial(self):
        for property in self:
            property._is_commercial = property.property_type_id.id==self.env.ref('real_estate.property_type_commercial').id

    # Compute Total Area
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        """Computes the total property area by adding living area and garden area."""
        for property in self:
            property.total_area = property.living_area + property.garden_area

    # Compute Best Offer Price
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        """Computes the highest offer price received for the property."""
        for property in self:
            valid_offers = property.offer_ids.filtered(lambda offer: offer.status!='reject')
            property.best_price = max(valid_offers.mapped('price'), default=0.0)

    # Onchange Method for Garden Fields
    @api.onchange('garden')
    def _onchange_garden_area_orientation(self):
        """Automatically set default garden area and orientation when garden is selected."""
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # Button Actions
    def action_cancel_button(self):
        """Cancel the property sale. Prevent cancellation if the property is already sold."""
        if self.state == 'sold':
            raise UserError("Sold properties cannot be cancelled.")
        self.state = 'cancelled'
    def action_sold_button(self):
        """Mark the property as sold. Prevent selling if the property is cancelled."""
        if self.state == 'cancelled':
            raise UserError("Cancelled properties cannot be sold.")
        self.state = 'sold'

    # Constraint on Selling Price
    @api.constrains('selling_price', 'expected_price')
    def check_selling_price(self):
        """Ensure the selling price is at least 90% of the expected price."""
        for property in self:
            if (
                not float_is_zero(property.selling_price, precision_rounding=0.01)
                and float_compare(
                    property.selling_price,
                    property.expected_price * 0.9,
                    precision_rounding=2
                ) == -1
            ):
                raise ValidationError(
                    "The selling price must be at least 90% of the expected price! "
                    "You must reduce the expected price if you want to accept this offer."
                )

    # Restrict Deletion of Properties
    @api.ondelete(at_uninstall=False)
    def _restrict_property_unlink(self):
        """Prevent deletion of properties that are not in 'New' or 'Cancelled' state."""
        if any(property.state not in ('new', 'cancelled') for property in self):
            raise UserError(
                "You cannot delete a property unless its state is 'New' or 'Cancelled'."
            )
