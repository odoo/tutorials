from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Property"
    _order = "id desc"

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "Expected price must be positive."),
        ("check_selling_price", "CHECK(selling_price >= 0)", "Selling price cannot be negative.")
    ]

    name = fields.Char(
        string="Name", required=True,
        help="Enter the property name."
    )
    description = fields.Text(
        string="Description", help="Brief description of the property."
    )
    postcode = fields.Char(
        string="Postcode", help="Postal code of the property."
    )
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Datetime.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(
        string="Expected Price", required=True,
        help="The price the seller expects."
    )
    selling_price = fields.Float(
        string="Selling Price", readonly=True, copy=False,
        help="The final selling price of the property."
    )
    bedrooms = fields.Integer(
        string="Bedrooms", default=2,
        help="Number of bedrooms in the property."
    )
    living_area = fields.Integer(
        string="Living Area (sq ft)", default=0,
        help="The size of the living area in square feet."
    )
    facades = fields.Integer(
        string="Facades", help="Number of facades the property has."
    )
    garage = fields.Boolean(
        string="Garage", help="Check if the property has a garage."
    )
    garden = fields.Boolean(
        string="Garden", help="Check if the property has a garden."
    )
    garden_area = fields.Integer(
        string="Garden Area (sq ft)",
        help="Size of the garden in square feet."
    )
    active = fields.Boolean(string="Active", default=True)
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ],
        string="Garden Orientation",
        help="Direction the garden faces."
    )
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled")
        ],
        string="State",
        required=True,
        default="new",
        copy=False
    )
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type",
        help="Type of the Property"
    )
    is_commercial = fields.Boolean(compute="_compute_is_commercial", store=True)
    buyer_id = fields.Many2one(
        'res.partner', string="Buyer", copy=False,
        help="Buyer of the Property", 
        domain="[('is_company', '=', is_commercial)]"
    )
    salesperson_id = fields.Many2one(
        'res.users', string="Salesperson",
        default=lambda self: self.env.user,
        help="Salesperson for the property"
    )
    tag_ids = fields.Many2many(
        'estate.property.tag', string="Property Tags",
        help="Tags for the Property"
    )
    offer_ids = fields.One2many(
        'estate.property.offer', 'property_id',
        string="Offers"
    )
    total_area = fields.Float(
        compute="_compute_total_area"
    )
    best_price = fields.Float(
        string = "Best Offer",
        compute="_compute_best_price",
    )
    company_id = fields.Many2one(
        'res.company', 
        string="Company", 
        default=lambda self: self.env.company, 
        index=True
    )
    
    @api.depends("property_type_id")
    def _compute_is_commercial(self):
        for property in self:
            property.is_commercial = property.property_type_id.name == 'commercial'

    # Compute the total area 
    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    # Compute the best price among the offers
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price'), default=0.00)
    
    # Change garden area and garden orientation on change of garden
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Cancelled Properties cannot be sold")
            record.state = 'sold'

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold Properties cannot be Cancelled")
            record.state = 'cancelled'
    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if (
                record.selling_price > 0 
                and float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0
            ):
                raise ValidationError("Selling Price must be 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def _prevent_unlink(self):
        if any(property.state not in ('new', 'cancelled') for property in self):
            raise UserError("You cannot delete the property")
