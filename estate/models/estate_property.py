"""module for the estate property model"""

from odoo import models, fields, api

class EstateProperty(models.Model):
    "Estate property odoo model"
    _name = "estate.property"
    _description= "model for real estate assets"
    #
    name = fields.Char("Name", required = True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", default = lambda _: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float("Expected Price", required = True)
    selling_price = fields.Float("Selling Price")
    bedrooms = fields.Integer("# bedrooms", default = 2)
    living_area = fields.Integer("Living Area (m2)")
    facades = fields.Integer("# facades")
    garage = fields.Boolean("Has Garage")
    garden = fields.Boolean("Has Garden")
    garden_area = fields.Integer("Garden Area (m2)")
    garden_orientation = fields.Selection([ ("north", "North"), ("south", "South"), ("east", "East"), ("west", "West") ])
    active = fields.Boolean(default = True)
    state = fields.Selection([ ("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("canceled", "Canceled") ], required = True, default = "new", string = "Bar", copy=False)
    create_date = fields.Datetime(copy = False)
    type_id = fields.Many2one("estate.property.type", string = "Type")
    buyer_id = fields.Many2one("res.partner", string = "Buyer")
    salesperson_id = fields.Many2one("res.users", string = "Salesperson", default = lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string = "Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string = "Offers")
    best_price = fields.Float("Best Offer", compute="_best_price")
    total_area = fields.Float("Total Area (m2)", compute="_total_area", default=0.0)
    #
    @api.depends("living_area", "garden_area")
    def _total_area(self):
        self.total_area = self.living_area + self.garden_area
    #
    @api.depends("offer_ids.price")
    def _best_price(self):
        self.best_price = max((of.price for of in self.offer_ids), default=0.0)
    #
