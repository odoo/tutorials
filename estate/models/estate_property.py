from odoo import api, fields, models
from odoo.tools import float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)',
        'The selling price must be strictly positive.'),
    ]

    name = fields.Char(
        "Title", required=True,
        help="This field specifies the estate property name.",
    )
    description = fields.Text(
        "Description",
        help="This field specifies the description of property in brief to provide insights on the property.",
    )
    postcode = fields.Char(
        "Postcode", help="This field specifies the postcode of the property address."
    )
    date_availability = fields.Date(
        "Available From", readonly=False, default=fields.Date.add(fields.Date.today(),months=3),
        help="This field specifies the date when the property will be available.", tracking=True,
    )
    expected_price = fields.Float(
        "Expected Price", required=True,
        help="This field specifies the price expected for the property.", tracking=True,
    )
    selling_price = fields.Float(
        "Selling Price", readonly=True, copy=False,
        help="This field specifies the actual selling price of the property.", tracking=True,
    )
    bedrooms = fields.Integer(
        "Bedrooms", default=2,
        help="This field specifies the number of bedroom that this property consists of.",
    )
    living_area = fields.Integer(
        "Living Area (sqm)",
        help="This field specifies the size of living area (in sqm.) of the property.",
    )
    facades = fields.Integer(
        "Facades",
        help="This field specifies the facade i.e. the exterior or the front of a property.",
    )
    garage = fields.Boolean(
        "Garage",
        help="This field specifies if the property has a garage",
    )
    garden = fields.Boolean(
        "Garden",
        help="This field specifies if the property has a garden",
    )
    garden_area = fields.Integer(
        "Garden Area (sqm)",
        help="This field specifies the size of garden area (in sqm.) of the property.",
    )
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="This selection fields specifies the facing direction of garden (North, South, East, or West).",
    )
    state = fields.Selection(
        string="Property Status", copy=False, required=True, default="new",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        help="This selection fields specifies the state of the property.", tracking=True,
    )
    active = fields.Boolean(
        "Active", default=True,
        help="This specifies if the property should be listed.", tracking=True,
    )
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type",
        help="This specifies the type of the property."
    )
    buyer_id = fields.Many2one(
        "res.partner", string="Buyer", copy=False,
        help="Buyer of the property.", tracking=True,
    )
    salesperson_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user,
        help="Sales Person associated with the property.", tracking=True,
    )
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Property Offers", tracking=True,)
    total_area = fields.Integer(
        "Total Area (sqm)", compute="_compute_total_area",
        help="This field specifies the total area (in sqm.) of the property.",
    )
    best_price = fields.Float(
        "Best Offer", compute="_compute_best_price",
        help="This field specifies the best offered price for the property.", tracking=True,
    )
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company,
        help="This field specifies the company to which the property belongs.", tracking=True,)
    image = fields.Image(string="Property Image")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for line in self:
            line.total_area = line.living_area + line.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for line in self:
            line.best_price = max(line.mapped('offer_ids.price'), default=0)

    # @api.onchange("garden")
    # def _onchange_garden(self):
    #     if self.garden:
    #         self.garden_area = 10
    #         self.garden_orientation = "north"
    #     else:
    #         self.garden_area = 0
    #         self.garden_orientation = False

    @api.constrains('selling_price', 'expected_price')
    def _check_smaller_selling_price(self):
        for line in self:
            if (float_compare(line.selling_price, line.expected_price * 0.9, precision_digits=2) == -1
                and not float_is_zero(line.selling_price, precision_rounding=2)):
                raise ValidationError('The selling price must be atleast 90% of the expected price. You must reduce the expected price if you want to accept this offer.')

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_cancelled(self):
        for line in self:
            if line.state not in ('new', 'cancelled'):
                raise UserError('Only new and cancelled properties can be deleted.')

    def action_cancel(self):
        self.ensure_one()

        if self.state == 'sold':
            raise UserError("Sold Property cannot be cancelled.")
        else:
            self.state = 'cancelled'

        return True

    def action_sold(self):
        self.ensure_one()

        if self.state == 'cancelled':
            raise UserError("Cancelled Property cannot be sold.")
        elif self.state != 'offer_accepted':
            raise UserError("Please accept an offer first.")
        else:
            self.state = 'sold'

        return True
