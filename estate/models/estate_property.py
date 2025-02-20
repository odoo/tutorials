from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'
    _rec_name = 'name'
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', "The expected price must be greater then 0."),
        ('check_selling_price', 'CHECK(selling_price >= 0)', "The selling price must be greater then 0."),
    ]

    name = fields.Char(required=True, string="Property Name")
    active = fields.Boolean(default=True, string="is Active")

    property_type_id = fields.Many2one(
        comodel_name="estate.property.type", 
        string="Property Type"
    )
    property_tag_ids = fields.Many2many(
        comodel_name="estate.property.tag", 
        string="Property Tags"
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offers", 
        inverse_name="property_id", 
        string="Offers"
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        default=lambda self: self.env.user
    )
    partner_id = fields.Many2one("res.partner", string="Partner")
    company_id = fields.Many2one(
        string="Company",
        comodel_name='res.company'
    )

    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postal Code")
    date_availability = fields.Date(
        string="Availability Date", 
        default=lambda self: fields.Date.today() + relativedelta(months=3),
        copy=False
    )
    
    expected_price = fields.Float(string="Expected Price", required=True)
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price")
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=2)
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
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
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

    # find max offered price
    @api.depends("offer_ids")
    def _compute_best_price(self):
        for property in self:
            price_list = property.offer_ids.mapped('price')
            property.best_price = max(price_list) if price_list else 0

    # sets default value when garden is enabled 
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'

    # checks if selling price is greater then or equal to 90% expected price
    @api.constrains("selling_price")
    def check_selling_price(self):
        if any(property.selling_price < (property.expected_price * 0.90) for property in self):
            raise ValidationError(
                "The selling price must be 90'%' of expected price."
                " You must Lower the expected price to accpect offer."
            )
        
    @api.constrains("property_type_id", "partner_id")
    def check_partner_id(self):
        for property in self:
            if property.property_type_id.id  == property.env.ref('estate.property_type_commercial').id:
                if property.partner_id and property.partner_id.company_type != 'company':
                    raise UserError("When a property is of commercial type, the partner must be a company.")

    # Prevent delete if property is in new or cancelled state
    @api.ondelete(at_uninstall=False)
    def check_on_delete(self):
        for property in self:
            if property.state == 'new' or property.state =='cancelled':
                raise UserError("Can't perform this operation!!")

    # sets property state to sold
    def action_property_sold(self):
        for property in self:
            if property.state == 'cancelled':   
                raise UserError(message="Cancelled property can't be sold.")
            else:
                property.state = 'sold'

    # sets property state to cancelled
    def action_property_cancel(self):
        self.state = 'cancelled'

    def _accept_offer(self):
        expried_properties = self.search([
            ('date_availability', '<=', fields.Date.today()),
            ('offer_ids.state', '!=', 'accepted'),
            ('state', '=' , 'received'), 
        ])
        for property in expried_properties:
            best_offer = property.offer_ids.filtered(lambda offer : offer.state !='refused').sorted('price', reverse=True)[:1]
            
            if best_offer:
                best_offer.action_offer_confirm()
