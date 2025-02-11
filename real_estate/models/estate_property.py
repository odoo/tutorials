from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Property"
    _order = 'id desc'
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >0)', 'The Expected Price must be strickly Positive.'),
        ('check_selling_price', 'CHECK(selling_price >=0)', 'The Selling Price must be Positive.')
    ]

    # Description
    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Property Description")
    postcode = fields.Char(string="Postcode") 
    date_availability = fields.Date(string="Availabile From",copy=False,
        default=lambda self:fields.Datetime.today() + relativedelta(months=3)
    )

    expected_price = fields.Float(string="Expected Price",required=True)
    selling_price = fields.Float(string="Selling Price",readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms",default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"), 
            ('west', "West")
        ]
    )
    total_area = fields.Integer(compute='_compute_total_area')
    active = fields.Boolean(string="Active", default=True)
    state = fields.Selection(string='State',
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled")
        ],
        required=True,
        default="new",
        copy=False
    )
    
    property_type_id = fields.Many2one('estate.property.type',string="Property Type")
    property_tag_ids = fields.Many2many('estate.property.tag',string="Property Tags")
    offer_ids = fields.One2many('estate.property.offer','property_id')
    user_id = fields.Many2one('res.users', string='Salesperson',
        default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one('res.partner',string="Buyers")
    best_offer = fields.Float(string="Best Offer", compute='_compute_best_offer', store=True)

    # Computing Total Area from living_area and garden_area
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    # Highest Offer Price from all the offers 
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped('price'), default=0.0)

    # Change garden_area and garden_orientation when garden field change
    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # action to change state:canceled
    def action_cancel(self):
        self.state = 'cancelled'

    # action to change state:sold
    def action_sold(self):
        if self.state == 'cancelled':
            raise UserError("Cancelled Property can not be sold")
        else:
            self.state = 'sold'


    # checks that selling price cannot be lower than 90% of the expected price.
    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for property in self:
            if (
                not float_is_zero(property.selling_price, precision_rounding=0.01)
                and float_compare(
                    property.selling_price,
                    property.expected_price * 0.9, # 90% of the expected price
                    precision_rounding=0.01
                ) == -1
            ):
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price."
                )
