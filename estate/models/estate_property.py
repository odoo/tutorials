from odoo import models, fields, api, exceptions
from datetime import date, timedelta
from odoo.exceptions import ValidationError
class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Damn this model is good for doing real estate related stuff"
    _order = "id desc"

    name = fields.Char(name = "Title", required=True)
    description = fields.Text(name = "Description", required = True)
    postcode = fields.Char(name = "PostCode", required = True)
    date_availability = fields.Date(name = "Availability", default=lambda self: date.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(name="Expected Price")
    selling_price = fields.Float(name = "Selling Price", readonly = True, copy = False)
    bedrooms = fields.Integer(name = "Bedrooms", default = 2)
    living_area = fields.Integer(name = "Living Area (m²)")
    facades = fields.Integer(name = "Facades")
    garage = fields.Boolean(name = "Garage")
    garden = fields.Boolean(name = "Garden")
    garden_area = fields.Integer(name = "Garden Area (m²)")
    garden_orientation = fields.Selection(string='Garden orientation',
        selection=[('north', 'North'), 
                   ('west', 'West'), ('south', 'South'), 
                   ('east', 'East')
                   ],
        help="Chose the direct which the garden is facing")
    
    active = fields.Boolean(default=True)
    state = fields.Selection(string='Status',
        selection=[('new', 'New'), 
                   ('offer received', 'Offer received'), 
                   ('offer accepted', 'Offer accepted'), 
                   ('sold', 'Sold'), 
                   ('cancelled', 'Cancelled')
                   ],
                   default='new',
        help="Is the house sold already ?")
    type_id = fields.Many2one("estate.property.types", string = "Property Type")
    sales_person_id = fields.Many2one("res.users", string = "Sales Person", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string = "Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags", name="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", name="Offers")
    total_area = fields.Float(compute="_compute_total_area", string="Total Area (m²)")
    best_price = fields.Float(compute="_compute_best_price", string="Best price")
    salesperson_id = fields.Many2one("res.users", string="Salesperson")


    _sql_constraints = [
        ('positive_expected_price',
        'CHECK (expected_price>0)',
        'The expected price should always be positive!'),
        ('positive_selling_price',
        'CHECK (selling_price>0)',
        'The selling price should always be positive!'),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area
    
    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False
    
    @api.constrains('selling_price')
    def check_selling_price_not_lower_than_90_percent_of_expected_price(self):
        for record in self:
            if record.selling_price < 0.9 * record.expected_price:
                raise ValidationError("The selling price must be at least 90% of the expected price")
    
    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_is_new_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise ValidationError("You can't delete a property in this state")

    def cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("A sold property can't be cancelled")
            else:
                record.state = "cancelled"
    def sold_property(self):
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError("A cancelled property can't be sold")
            else:
                record.state = "sold"
    def set_buyer(self, buyer):
        self.buyer_id=buyer
    def set_status(self, status):
        self.state = status
    def set_sold_price(self, price):
        self.selling_price = price
    def get_status(self):
        return self.state
