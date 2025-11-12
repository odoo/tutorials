# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Property"
    _order = 'id desc'
    _sql_constraints = [
        ('check_expected_price', "CHECK(expected_price > 0)", "The expected price must be strictly positive."),
        ('check_selling_price', "CHECK(selling_price >= 0)", "The selling price must be positive."),
    ]

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date Availability", copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True , copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection(
        selection=[ 
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ], 
        string="Garden Orientation"
    )
    state = fields.Selection(
        selection=[  
            ('new', "New"),  
            ('offer_received', "Offer Received"),  
            ('offer_accepted', "Offer Accepted"),  
            ('sold', "Sold"),  
            ('cancelled', "Cancelled")  
        ],  
        default='new',  
        required=True  
    )
    active = fields.Boolean(string = 'Active', default=True)
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type"
    )
    buyer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Buyer"
    )
    salesperson_id = fields.Many2one(
        comodel_name="res.users",
        default=lambda self: self.env.user,
        string="Salesperson"
    )
    property_tag_ids = fields.Many2many(
        comodel_name="estate.property.tag",
        string="Property Tag"
    )
    property_offer_ids = fields.One2many(
        comodel_name="estate.property.offer", 
        inverse_name="property_id",
        string="Offers"
    )
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer", store=True)
    image = fields.Image(string="Property Image",
         max_width=1024, 
         max_height=1024
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        required=True, default=lambda self: self.env.company, 
        help="This field specifies the company to which the property belongs."
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('property_offer_ids.price')
    def _compute_best_offer(self):
        for offer in self:
            offer.best_offer= max(offer.property_offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise UserError(_("Sold properties cannot be cancelled."))
            property.state = 'cancelled'

    def action_sold(self):
        for property in self:
            if property.state == 'cancelled':
                raise UserError(_("Cancelled properties cannot be sold."))
            elif 'accepted' not in [offer.status for offer in property.property_offer_ids]:
                raise UserError(_("You cannot sell the property without an accepted offer."))
            else: 
                property.state = 'sold' 

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        if any(property.selling_price and property.selling_price < 0.9 * property.expected_price for property in self):
                raise ValidationError(_("The selling price cannot be lower than 90% of the expected price."))

    @api.ondelete(at_uninstall=False)
    def _restrict_property_unlink(self):
        for property in self:
            if property.state not in ['new', 'cancelled']:
                raise exceptions.UserError(_("You can only delete properties that are New or Cancelled."))
