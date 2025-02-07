from odoo import api, exceptions, fields, models
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Property"

    # Description
    name = fields.Char(
        string="Property Name",
        required=True)
    description = fields.Text(
        string="Property Description")
    postcode = fields.Char(
        string="Postcode") 
    date_availability = fields.Date(
        string="Availabile From",
        copy=False,
        default=lambda self:fields.Datetime.today() + relativedelta(months=3)
    )

    expected_price = fields.Float(
        string="Expected Price",
        required=True)
    selling_price = fields.Float(
        string="Selling Price",
        readonly=True, 
        copy=False)
    bedrooms = fields.Integer(
        string="Bedrooms",
        default=2)
    living_area = fields.Integer(
        string="Living Area")
    facades = fields.Integer(
        string="Facades")
    garage = fields.Boolean(
        string="Garage")
    garden = fields.Boolean(
        string="Garden")
    garden_area = fields.Integer(
        string="Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"), 
            ('west', "West")
        ]
    )
    total_area = fields.Float(
        compute='_compute_total_area')
    active = fields.Boolean(
        string="Active", 
        default=True)
    state = fields.Selection(
        string='State',
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
    
    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Property Type")
    property_tag_ids = fields.Many2many(
        'estate.property.tag',
        string="Property Tags")
    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id')
    user_id = fields.Many2one(
        'res.users', 
        string='Salesperson',
        index=True,
        tracking=True,
        default=lambda self: self.env.user)
    buyer_id = fields.Many2one(
        'res.partner',
        string="Buyers",
        index=True,
        tracking=True)
    best_offer = fields.Float(
        string="Best Offer",
        compute='_compute_best_offer',
        store=True)


    # Computing Total Area from living_area and garden_area
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # Highest Offer Price from all the offers 
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0.0)

    # Change garden_area and garden_orientation when garden field change
    @api.onchange('garden')
    def _onchange_garden(self):
        print("Garden fields changed: ", self.garden)
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
        if self.state == "cancelled":
            raise exceptions.UserError("Cancelled Property can not be sold")
        else:
            self.state = 'sold'
