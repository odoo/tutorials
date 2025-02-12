from odoo import api, models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "id desc"

    def calculate_three_months_later():
        today = datetime.now()
        return today + relativedelta(months=3)

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode", group_expand=True)
    date_availability = fields.Date(string="Date Availability", default=calculate_three_months_later(), copy=False)
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    
    garden_orientation = fields.Selection(
        string="Garden Orientation", 
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]);
    
    active = fields.Boolean(string="Is Active", default=True)
    
    state = fields.Selection(
        string="State", 
        required=True, 
        copy=False,
        default="new",
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')])

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    property_offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(string="Toatal Area (sqm)", compute="_compute_total_area")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('property_offer_ids')
    def _compute_best_offer(self):
        for record in self:
            if record.property_offer_ids:
                record.best_offer = max(record.property_offer_ids.mapped('price'), default=0)
            else:
                record.best_offer = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:    
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    # Action Button Methods
    # This methods were used earlier for different sold and cancel button of the property form
    def action_set_sold_status(self):
        if self.state == 'cancelled':
            raise UserError('A cancelled property cannot be sold.')
        else:
            self.state = 'sold'

    def action_set_cancelled_status(self):
        if self.state == 'sold':
            raise UserError('A sold property cannot be cancelled.')
        else:
            self.state = 'cancelled'

    # Single method for two buttons action handling
    def action_set_status(self):
        if self.env.context.get('button_id') == 'sold_button':
            if self.state == 'cancelled':
                raise UserError('A cancelled property cannot be sold.')
            else:
                self.state = 'sold'
        elif self.env.context.get('button_id') == 'cancelled_button':
            if self.state == 'sold':
                raise UserError('A sold property cannot be cancelled.')
            else:
                self.state = 'cancelled'

    # Python Constraints
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                    raise ValidationError("The selling price must be greater than the 90% of expected price.")

    @api.ondelete(at_uninstall=False)
    def _delete_property(self):
        if self.state != 'new' and self.state != 'cancelled':
            raise UserError("Only new and cancelled propeties can be deleted.")
