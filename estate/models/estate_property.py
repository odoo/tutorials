
from odoo import api, fields, models
from datetime import timedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property Model"

    name = fields.Char(required=True)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", required=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers", help="All offers received for this property")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available From", copy=False , default= lambda self: fields.Date.today() + timedelta(90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True) 
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection(selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")])
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(selection=[("new", "New"), ("offer received", "Offer Received"), ("offer accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")], required=True, default="new", copy=False, string="Status" )
    total_area = fields.Integer(string="Total Area(sqm)", compute="_compute_total")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price")
    
    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
            
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                #mapped method takes the values of that specific column
                record.best_price = max(record.offer_ids.mapped("price"))
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
                            
                
                    



