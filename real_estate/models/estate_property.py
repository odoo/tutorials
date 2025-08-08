from odoo import models, fields, api
from odoo.exceptions import UserError  

from datetime import date

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True , copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    Active = fields.Boolean(default=False)
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(string="Best Offer Price",  store=True)
    active = fields.Boolean(default=True)

    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'),('east', 'East'),('west','West')],)

    state = fields.Selection([
    ('new', 'New'),
    ('offer_received', 'Offer Received'),
    ('offer_accepted', 'Offer Accepted'),
    ('sold', 'Sold'),
    ('cancelled', 'Cancelled')  
], string="Status", default="new")
  
                                                                                                                                                                                
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson" , default=lambda self: self.env.user)
    tag_id = fields.Many2many("estate.property.tag", string="Tags")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

   
    total_area= fields.Float(compute="_compute_total_area", readonly=True, copy=False)
    best_price= fields.Float(compute="_compute_best_price", readonly=True, default= 0.0)

    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price >= 0 )', 'A property selling price must be positive'),
        ('check_expected_price', 'CHECK(expected_price > 0 )', 'A property expected price must bepositive')
    ]

    @api.constrains('selling_price')
    def check_selling_price(self):
        if self.selling_price < (0.90*self.expected_price):
            raise UserError("selling price cannot be lower than 90% of the expected price.")


    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area= record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)


    @api.onchange("garden")
    def _change_garden(self):
        if(self.garden):
            self.garden_area=10
            self.garden_orientation="north"
        else:
            self.garden_area=0
            self.garden_orientation=False

    def mark_sold(self):
        if self.state != "cancelled":
            self.state = "sold"
        else:
            raise UserError("Cancelled properties cannot be sold")

        return True

    def mark_cancel(self):
        self.state = "cancelled"
        return True