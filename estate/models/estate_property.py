from odoo import api,fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property details"
    _order = "id desc"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description", required=True)
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From", copy=False, default=fields.Date.add(fields.Date.today(), months=3)) 
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False) 
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"), 
            ("south", "South"), 
            ("east", "East"), 
            ("west", "West")
        ]
    )
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        required=True,
        copy=False,
        default="new"
    )
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    user_id = fields.Many2one("res.users", string="Salesperson",default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Buyer")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    offer_count = fields.Integer(string="Count")
    
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area")
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0 

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False


    def property_action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("A sold property cannot be cancelled.")
            record.state = 'cancelled'

    def property_action_sell(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("A cancelled property cannot be sold.")
            record.state = 'sold'

    @api.onchange('offer_ids')
    def _onchange_offer(self):
        self.offer_count = len(self.offer_ids)

    sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive.'),
        ('check_bedroom', 'CHECK( bedroom >= 0)', ' Bedroom must be positive.'),
        ('check_living_area', 'CHECK(living_area > 0)', 'Living_area must be positive.'),
        ('check_facades', 'CHECK(facades >= 0)', 'Facades must be positive.'),
        ('check_garden_area', 'CHECK(garden_area > 0)', 'Garden_area must be positive.'),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2): 
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                    raise models.ValidationError(
                        "The selling price cannot be lower than 90% of the expected price!"
                    )

    @api.ondelete(at_uninstall=False)
    def _check_property_state_before_delete(self):
        for record in self:
            if record.state not in ["new", "cancelled"]:
                raise UserError(
                    "You cannot delete a property unless its state is 'New' or 'Cancelled'."
                )
                