from datetime import timedelta
from odoo import fields, models,api

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, 
        default=lambda self: fields.Date.today() + timedelta(days=90)
    )  # Default to 3 months from today
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)  # Default number of bedrooms is 2
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(default=True)  # Active field to manage visibility
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",  # Default state is 'New'
    )
    property_type_id = fields.Many2one(
        "estate.property.type", 
        string="Property Type"
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Property Tag"
    )
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer")

    # Add the One2many field to store the related offers
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    # Computed field for total_area
    total_area = fields.Float(string='Total Area', compute='_compute_total_area', store=True)

    # Computed field for find a best offer price 
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", store=True)


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)


    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            if property.offer_ids:
                property.best_price = max(property.offer_ids.mapped('price'))
            else:
                property.best_price = 0.0


    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10  # Default value for garden area
            self.garden_orientation = 'north'  # Default value for garden orientation
        else:
            self.garden_area = 0  # Clear the garden area
            self.garden_orientation = False  # Clear the garden orientation



    