from odoo import fields, models, api
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate App"
    
    #---------------------------------------------Basic Fields----------------------------------------#
    name = fields.Char(required=True)
    description = fields.Text() 
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default= lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    facades = fields.Integer()
    is_garage = fields.Boolean()
    is_garden = fields.Boolean()
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
    
    display_unit = fields.Selection([
        ('sqm', 'Square Meters'),
        ('sqft', 'Square Feet')
    ], default='sqm', string="Display Unit")  

    #-------------------------------------------Computed Fields--------------------------------------------# 
    living_area = fields.Float(compute="_compute_display_areas", inverse="_inverse_living_area", string="Living Area", default = 0.0, store=True)
    garden_area = fields.Float(compute="_compute_display_areas", inverse="_inverse_garden_area", string="Garden Area", default = 0.0, store=True)
    total_area = fields.Float(compute="_compute_display_areas", string= "Total Area", store=True)
    best_price = fields.Float(compute="_compute_best_price", string= "Best Price")

    #--------------------------------------------Relational Fields------------------------------------------#
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    seller_id = fields.Many2one("res.users", default=lambda self: self.env.user, string="Salesman")  
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")  
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    
    # --------------------------------------------Decorator Methods----------------------------------------#
    @api.depends("living_area", "garden_area", "display_unit")
    def _compute_display_areas(self):  
        for property in self:
            if property.display_unit == "sqft":
                property.living_area = property.living_area * 10.764
                property.garden_area = property.garden_area * 10.764
            else:
                property.living_area = property.living_area / 10.764
                property.garden_area = property.garden_area / 10.764

            property.total_area = property.living_area + property.garden_area

    def _inverse_living_area(self):
        for property in self:
            if property.display_unit == "sqft":
                property.living_area /= 10.764
              

    def _inverse_garden_area(self):
        for property in self:
            if property.display_unit == "sqft":
                property.garden_area /= 10.764  

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for prop in self:
            prop.best_price=max(prop.offer_ids.mapped("price")) if prop.offer_ids else 0.0
            
# --------------------------------------------Onchange methods------------------------------------#
    @api.onchange("is_garden")
    def _onchange_garden_present(self):
        if self.is_garden :
            self.garden_area = 10
            self.garden_orientation = 'north'
        else :
            self.garden_area = 0
            self.garden_orientation = False