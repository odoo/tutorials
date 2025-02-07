import datetime
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError

class EstateProperty(models.Model):

    _name = 'estate.property'
    _description = "Real Estate Property"

    name = fields.Char(
        string="Name",
        required=True,
        help="Enter the name of the property"
    )
    description = fields.Text(
        string="Description",
        required=True,
        help="Provide a detailed description of the property"
    )
    postcode = fields.Char(
        string="Postcode",
        required=True,
        help="Enter the postcode of the property"
    )
    date_availability = fields.Date(
        string="Date of Availability",
        required=True,
        copy=False,
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=+3),
        help="Specify when the property will be available"
    )
    expected_price = fields.Float(
        string="Expected Price",
        required=True,
        help="Enter the expected price of the property"
    )
    selling_price = fields.Float(
        string="Selling Price",
        readonly=True,
        copy=False,
        help="Enter the selling price of the property"
    )
    bedrooms = fields.Integer(
        string="Bedrooms",
        required=True,
        default=2,
        help="Enter the number of bedrooms"
    )
    living_area = fields.Integer(
        string="Living Area (sq meters)",
        required=True,
        help="Enter the living area of the property"
    )

    facades = fields.Integer(
        string="Number of Facades",
        required=True,
        help="Enter the number of facades the property has"
    )
    garage = fields.Boolean(
        string="Has Garage",
        help="Check if the property has a garage"
    )
    garden = fields.Boolean(
        string="Has Garden",
        help="Check if the property has a garden"
    )
    garden_area = fields.Integer(
        string="Garden Area (sq meters)",
        required=True,
        help="Enter the area of the garden"
    )
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation",
        required=True, help="Select the orientation of the garden"
    )
    active = fields.Boolean(
        string="Active",
        default=True,
        help="If unchecked, it will archive the property."
    )
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        string="State",
        required=True,
        default='new',
        copy=False,
        help="Current state of the property."
    )

    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        string="Property Type"
    )
    buyer_id = fields.Many2one(
        comodel_name='res.partner',
        string="Buyer",
        copy=False
    )
    salesperson_id = fields.Many2one(
        comodel_name='res.users',
        string="Salesperson",
        default=lambda self: self.env.user
    )

    tag_ids = fields.Many2many(
        comodel_name='estate.property.tag',
        string="Tag"
    )

    offer_ids = fields.One2many(
        comodel_name='estate.property.offer',
        inverse_name='property_id',
        string="Offers"
    )

    total_area = fields.Float(
        string="Total Area",
        compute='_compute_total_area'
    )
    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    best_price = fields.Float(
        string="Best Offer",
        compute='_compute_best_price',
    )
    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if(record.offer_ids):
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if (self.garden):
            self.garden_orientation = 'north'
            self.garden_area=10
        else:
            self.garden_orientation = False
            self.garden_area = 0

    def action_set_sold(self):
        for record in self:
            if (record.state == "cancelled" or record.state == "Cancelled"):
                raise UserError('Cancelled Property can not be sold')
            record.state = 'sold'
        
    def action_set_cancel(self):
        for record in self:
            if(record.state == "sold" or record.state == "Sold"):
                raise UserError('Sold Property can not be cancel')
            record.state = 'cancelled'
