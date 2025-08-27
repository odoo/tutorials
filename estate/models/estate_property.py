from datetime import datetime, timedelta
from odoo import api, fields, models

# estate.property model 
class estateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property database table"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default= datetime.now() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West')
            ])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        default="new",
        copy=False,
        required=True,
        selection=[
            ('new','New'), 
            ('offer_recieved','Offer Received'), 
            ('offer_accepted','Offer Accepted'), 
            ('sold_and_cancelled','Sold and Cancelled')
            ],
        help="State of the property")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                for offer in record.offer_ids:
                    if offer.price > record.best_price:
                        record.best_price = offer.price
            else:
                record.best_price = 0.0
    
    @api.onchange("garden")
    def _comoute_garden(self):
        if self.garden is True:
            self.garden_orientation = "north"
            self.garden_area = 10
        else:
            self.garden_orientation = False
            self.garden_area = 0

