from odoo import fields, models, api # type: ignore
from odoo.exceptions import ValidationError, UserError # type: ignore
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate App"
    _order = "id desc"
    _sql_constraints = [
        ("check_selling_price","CHECK(selling_price >= 0)","Selling Price must be a positive amount"),
        ("check_expected_price","CHECK(expected_price >= 0)","Expected Price must be a positive amount")
    ]
    
    #---------------------------------------------Basic Fields----------------------------------------#
    name = fields.Char(required=True, default='MY HOME')
    description = fields.Text(default="Big House in Mumbai") 
    postcode = fields.Char(default='123456')
    date_availability = fields.Date(copy=False, default=lambda self:fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True, default=100)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer(default=1)
    is_garage = fields.Boolean(default=False)
    is_garden = fields.Boolean(default=False)
    active = fields.Boolean(default=True)

    #--------------------------------------------Selection Fields---------------------------------------#
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation"
    )   
    state = fields.Selection([
        ('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'), ('cancelled', 'Cancelled')
    ], default='new')
    
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
    @api.depends("living_area", "garden_area", "measurement_unit")
    def _compute_total_area(self):  
        for property in self:
            property.total_area = property.living_area + property.garden_area
            if property.measurement_unit == 'sqft':
                property.total_area *= 10.764

    @api.depends("offer_ids.offer_price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price=max(prop.offer_ids.mapped("offer_price")) if prop.offer_ids else 0.0
            
#---------------------------------------------------- Action Methods----------------------------------------#
    def property_sold_action(self):  
        if self.state in ('sold'):
            raise UserError('Property is Already sold')
        self.state = "sold"
        return True

    def property_cancel_action(self):
        if self.state in ('cancelled'):
            raise UserError('Property is not for sale anymore')
        self.state = "cancelled"
        return True
    
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
            if fields.Float.compare (property.selling_price, property.expected_price * 90/100, precision_rounding=0.01) < 0 and not fields.Float.is_zero(property.selling_price, precision_rounding=0.01):
                raise ValidationError ("Selling Price cannot be lower than '90%'of the expected price.")
