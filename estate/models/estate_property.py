from odoo import fields
from odoo import models
from odoo import api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate App"
    _inherit = ['mail.thread']
    _sql_constraints = [
        ("check_selling_price","CHECK(selling_price >= 0)","Selling Price must be a positive amount"),
        ("check_expected_price","CHECK(expected_price >= 0)","Expected Price must be a positive amount")
    ]

    #---------------------------------------------Basic Fields----------------------------------------#
    name = fields.Char(required=True, default='MY HOME')
    description = fields.Text(default="Big House in Mumbai") 
    postcode = fields.Char(default='123456')
    date_availability = fields.Date(default=lambda self:fields.Date.today() + relativedelta(months=3), copy=False)
    expected_price = fields.Float(required=True, tracking=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer(default=1)
    is_garage = fields.Boolean(default=False)
    is_garden = fields.Boolean(default=False)
    active = fields.Boolean(default=True)
    image = fields.Image(string="Image")

    #--------------------------------------------Selection Fields---------------------------------------#
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )   
    state = fields.Selection([
        ('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'), ('cancelled', 'Cancelled')
    ], default='new', tracking=True)
    
    measurement_unit = fields.Selection([
        ('sqm', 'Square Meters'),
        ('sqft', 'Square Feet')
    ], default='sqm', string="Measurement Unit")  

    #-------------------------------------------Computed Fields--------------------------------------------# 
    living_area = fields.Float(string="Living Area", default = 0.0)
    garden_area = fields.Float(string="Garden Area", default = 0.0)
    total_area = fields.Float(compute = "_compute_total_area", string= "Total Area")
    best_price = fields.Float(compute="_compute_best_price", string= "Best Price")

    #--------------------------------------------Relational Fields------------------------------------------#
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    seller_id = fields.Many2one("res.users", default=lambda self: self.env.user, string="Salesman")  
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")  
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    
    # --------------------------------------------Compute Methods----------------------------------------#
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.offer_price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price=max(prop.offer_ids.mapped("offer_price")) if prop.offer_ids else 0.0
            
    #----------------------------------------------- Action Methods----------------------------------------#
    def action_property_sold(self):
        if self.state == 'sold':
            raise UserError('Property is Already sold')
        self.state = "sold"

    def action_property_cancel(self):
        if self.state == 'cancelled':
            raise UserError('Property is already cancelled')
        self.state = "cancelled"
    
    # --------------------------------------------Constrain and Onchange Methods------------------------------------------------#
    @api.onchange("is_garden")
    def _onchange_garden_present(self):
        if self.is_garden :
            self.garden_area = 10
            self.garden_orientation = 'north'
        else :
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price','expected_price')
    def _check_selling_price(self):
        for property in self:
            if property.selling_price and property.selling_price < property.expected_price * 0.90:
                raise ValidationError ("Selling Price cannot be lower than '90%'of the expected price.")

    #-------------------------------------CRUD methods------------------------------------------#
    @api.ondelete(at_uninstall=False)
    def _unlink_except_sold_or_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled'] :
                raise UserError("You can only delete New or Cancelled Properties")
