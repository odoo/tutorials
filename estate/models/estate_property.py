from datetime import timedelta
from odoo import api, exceptions, fields, models
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property Name"

    name = fields.Char('Property Name', required = True, size = 30)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode', size = 6)
    date_availability = fields.Date('Date Availability', copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float('Expected Price', required = True)
    selling_price = fields.Float('Selling Price', 
        readonly=True, 
        copy=False,
    )
    bedrooms = fields.Integer('Bedrooms', default = 2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden', default=False)
    garden_area = fields.Integer('Garden Area(sqm)', default = 0)
    total_area = fields.Integer('Total Area (sqm)', compute="_compute_total_area", store=True)
    garden_orientation = fields.Selection(
        string ='Type',
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')    
        ]
    )
    active = fields.Boolean('Active', 
        default=True, 
        help='if you want to active'
        )
    state = fields.Selection(
        required = True,    
        copy = False,
        default = "new",
        selection = [
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ]
    )
    salesman_id = fields.Many2one('res.users',default=lambda self: self.env.user, string='Salesman')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=True)
    tags_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", store=True)
    #computed fields
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0.0)
    #onchange
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False 
    #function for Sold and Cancelled Button 
    def action_set_status_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled Property cannot be Sold")
            record.state = "sold"
        return True 
    def action_set_status_cancel(self):
        for record in self:
            if record.state == "sold":
                message = "Sold Property cannot be Cancelled"
                raise UserError(message)
            else:
                record.state = "cancelled"
            return True
    #SQL constaints
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
    ]
    #Constaints
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            # check if selling_price is zero
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            # selling_price is at least 90% of expected_price
            min_acceptable_price = 0.9 * record.expected_price
            if float_compare(record.selling_price, min_acceptable_price, precision_rounding=0.01) < 0:
                raise ValidationError(
                    "The selling price cannot be less than 90% of the expected price."
                )