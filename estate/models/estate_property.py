from odoo import api, fields, models, exceptions

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _rec_name = 'property_name'
    _order = 'id desc'
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be greater then 0.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be greater then 0.'),
    ]

    property_name = fields.Char(required=True, string="Property Name")
    active = fields.Boolean(default=True, string="is Active")

    property_type_id = fields.Many2one(comodel_name="estate.property.type", string="Property Type")
    property_tag_id = fields.Many2many(comodel_name="estate.property.tag", string="Property Tags")
    offers_id= fields.One2many(comodel_name="estate.property.offers", inverse_name="property_id", string="Offers")
    salseperson_id= fields.Many2one("res.users", string="Salesperson")
    partner_id= fields.Many2one("res.partner", string="Partner")

    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postal Code")
    date_availability = fields.Date("Availability Date", copy=False, default= fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(string="Expected Price",required=True)
    best_price=fields.Float(string="Best Offer", compute="_compute_best_price", default=0)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms",default=2)
    living_area = fields.Integer(string="Living Area (feet²)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (feet²)")
    total_area = fields.Integer(string="Total Area (feet²)", compute="_compute_totalarea")

    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('west', 'West'),
            ('east', 'East')
        ]
    )

    state = fields.Selection(
        string= "State",
        selection=[
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ],
        default="new",
        copy=False
    )

    # compute the total area using garden area + living area
    @api.depends("garden_area", "living_area")
    def _compute_totalarea(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area
    
    # sets default value when garden is enabled 
    @api.onchange("garden")
    def _onchange_garden(self):
        for property in self:
            if property.garden:
                property.garden_area = 10
                property.garden_orientation = 'north'
    
    # find max offered price
    @api.depends("offers_id")
    def _compute_best_price(self):
        for property in self:
            property.best_price = max(property.offers_id.mapped('price')) if property.offers_id.mapped('price')  else 0

    # sets property state to sold
    def action_property_sold(self):
        for property in self:
            if property.state == 'cancelled' or property.state == 'Cancelled':   
                raise exceptions.UserError(message="Cancelled property can't be sold.")
            else:
                property.state = 'sold'
    
    # sets property state to cancelled
    def action_property_cancel(self):
        for property in self:
            if property.state:
                property.state = 'cancelled'

    # checks if selling price is greater then or equal to 90% expected price
    @api.constrains("selling_price")
    def check_selling_price(self):
        for property in self:
            if property.selling_price < (property.expected_price * 0.90):
                raise exceptions.ValidationError("The selling price must be 90'%' of expected price. You must lower the expected price to accpect offer. ")
