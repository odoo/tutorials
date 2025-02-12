from odoo import api, fields, models,exceptions
from datetime import datetime, timedelta
from odoo.tools.float_utils import float_compare, float_is_zero

class Property_Plan(models.Model):
    _name = "estate.property"
    _description = "Estate Model containing all the fields"

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    name = fields.Char(string="Title", required=True, help="Enter the name of property")
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date Availability", copy=False, default=lambda self: (datetime.today() + timedelta(days=90)).date())
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[("north","North"), ("south","South"),("east","East"),("west","West")],
        help="Type is used for direction"
    )
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
    best_price = fields.Float(string="Best Offer Price", compute="_compute_best_price", store=True)
    state = fields.Selection(string="State", selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')], required=True, copy=False)
    active = fields.Boolean(string="Active", default=True)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'  
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def change_state(self, new_state):
        """Generic method to change the state of the property with validation."""
        for record in self:
            if new_state == 'canceled' and record.state == 'sold':
                raise exceptions.UserError("Sold properties can't be canceled")
            elif new_state == 'sold' and record.state == 'canceled':
                raise exceptions.UserError("Canceled properties can't be sold")
            else:
                record.state = new_state

    def button_cancel_action(self):
        """Cancel the property."""
        self.change_state('canceled')

    def button_sold_action(self):
        """Mark the property as sold."""
        self.change_state('sold')

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', "The expected price must be strictly positive."),
        ('check_selling_price', 'CHECK(selling_price >= 0)', "The selling price must be positive."),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue


            min_acceptable_price = record.expected_price * 0.9
            
            # Compare selling_price with min_acceptable_price
            if float_compare(record.selling_price, min_acceptable_price, precision_digits=2) == -1:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )
