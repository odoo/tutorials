from datetime import  datetime, timedelta
from odoo import api, fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    living_area = fields.Float(string="Living Area (sqm)")
    garden_area = fields.Float(string="Garden Area (sqm)")
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area", store=True)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_type_id = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(string="Best Offer Price", compute="_compute_best_price", store=True)

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    price = fields.Float(string="Offer Price", required=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    seller_id = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user)
    # Read-Only 
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    availability_date = fields.Date(
        string="Availability Date",
        default=lambda self: datetime.today() + timedelta(days=90), #3 months
        copy=False
    )
    
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    bedrooms = fields.Integer(string="Bedrooms", default=2)    
    active = fields.Boolean(string="Active", default=True)
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float() 
#   living_area=fields.Integer()
    living_area=fields.Integer()
    # State Field with Selection
    state = fields.Selection([
        ('new', "New"),
        ('offer_received', "Offer Received"),
        ('offer_accepted', "Offer Accepted"),
        ('sold', "Sold"),
        ('cancelled', "Cancelled"),
    ], string="State", required=True, default='new', copy=False)
