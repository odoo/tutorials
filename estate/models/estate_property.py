from odoo import fields, api, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    # Basic Fields
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    
    # Date Fields
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.today() + relativedelta(months=3)
    )
    
    # Price Fields
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    
    # Property Details
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    
    # Selection Fields
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ],
        string="Garden Orientation"
    )
    
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        string="Status",
        required=True,
        copy=False,
        default='new'
    )
    
    active = fields.Boolean(string="Active", default=True)
    
    # Many2one, Many2many, One2many Relation to Property Type
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    
    salesperson_id = fields.Many2one(
    "res.users", 
    string="Salesperson", 
    default=lambda self: self.env.user
    )
    
    offer_ids = fields.One2many(
    "estate.property.offer",  
    "property_id",           
    string="Offers"
    )
    
    tag_ids = fields.Many2many("estate.property.tag", string="Tags", widget="many2many_tags" )
    
    # Computed Fields & Onchange
    
    total_area = fields.Float(string="Total Area",compute="_compute_total_area")
    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    best_price = fields.Float("Best Offer", compute="_compute_best_price", store=True)
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    # Onchange
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "North"
        else:
            self.garden_area = 0
            self.garden_orientation = False


    # Add Action Logic of "Cancel" & "Sold"
    
    def action_set_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Canceled property cannot be sold.")
            record.state = "sold"
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success',
                'message': 'The property has been marked as sold.',
                'sticky': False,
                'type': 'success',  
            }
        }

    def action_set_canceled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold property cannot be canceled.")
            record.state = "cancelled"
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Cancelled',
                'message': 'The property has been marked as canceled.',
                'sticky': False,
                'type': 'warning',  
            }
        }
        
        
        # SQL Constraints
        
    _sql_constraints = [
        (
            "check_expected_price_positive",
            "CHECK(expected_price > 0)",
            "The expected price must be strictly positive.",
        ),
        (
            "check_selling_price_positive",
            "CHECK(selling_price >= 0)",
            "The selling price must be positive.",
        ),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_threshold(self):
        for record in self:
            if record.selling_price:
                if float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_digits=2
                ) < 0:
                    raise ValidationError(
                        "The selling price cannot be lower than 90% of the expected price."
                    )