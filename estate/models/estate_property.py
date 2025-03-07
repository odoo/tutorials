from datetime import  datetime, timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc" 
    sequence = fields.Integer("Sequence", default=1, help="Used to order property types. Lower is better.")

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    living_area = fields.Float(string="Living Area (sqm)")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)", default=0)
    orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Orientation"
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_type_id = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    best_price = fields.Float(string="Best Offer Price", compute="_compute_best_price", store=True)
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area", store=True)

    price = fields.Float(string="Offer Price", required=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    seller_id = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user)
    # Read-Only 
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)

    availability_date = fields.Date(
        string="Availability Date",
        default=lambda self: datetime.today() + timedelta(days=90), #3 months
        copy=False
    )

    facades = fields.Integer()
    garage = fields.Boolean()
    # garden = fields.Boolean()
    # garden_area = fields.Integer()
    bedrooms = fields.Integer(string="Bedrooms", default=2)    
    active = fields.Boolean(string="Active", default=True)
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float() 
#   living_area=fields.Integer()
    living_area=fields.Integer()
    # State Field with Selection
    state = fields.Selection([
        ('new', "New"),
        ('offer_received', "Offer Received"),
        ('offer_accepted', "Offer Accepted"),
        ('sold', "Sold"),
        ('cancelled', "Cancelled"),
    ], string="State", required=True, default='new', copy=False)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.orientation = 'north'
        else:
            self.garden_area = 0
            self.orientation = False

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    
    def action_cancel(self):
        # Cancels the property and prevents selling it later.
        for record in self:
            if record.state == 'sold':
                raise UserError("A sold property cannot be canceled.")
            record.state = 'cancelled'

    def action_sold(self):
        # Marks the property as sold and prevents canceling it later.
        for record in self:
            if record.state == 'cancelled':
                raise UserError("Canceled properties cannot be sold.")
            record.state = 'sold'
    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.01):  # Ignore if selling price is 0
                min_acceptable_price = record.expected_price * 0.9
                if float_compare(record.selling_price, min_acceptable_price, precision_rounding=0.01) == -1:
                    raise models.ValidationError(
                        "Selling price cannot be lower than 90% of the expected price!"
                    )

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
    ]
    