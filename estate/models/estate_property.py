from datetime import  datetime, timedelta # used to calculate date 
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _inherit = ['mail.thread']
    _description = "Estate Property"
    _order = "id desc" 

    name = fields.Char(string="Name", required=True, tracking=True)
    sequence = fields.Integer("Sequence", default=1, help="Used to order property types. Lower is better.")
    description = fields.Text(string="Description")
    living_area = fields.Float(string="Living Area (sqm)")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)", default=0)
    orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Orientation"
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_type_ids = fields.Many2many("estate.property.tag", string="Property Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(string="Best Offer Price", compute="_compute_best_price", store="True") #Stores computed values in the database for faster access.
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area", store=True)
    price = fields.Float(string="Offer Price", required=True, default=0.0, tracking=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    seller_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        default=lambda self: self.env.company,
        required=True
    )
    image_url = fields.Char(string="Image URL")
    image_upload = fields.Image(string="Upload Image") 

    # Read-Only 
    selling_price = fields.Float(string="Selling Price")
    availability_date = fields.Date(
        string="Availability Date",
        default=lambda self: datetime.today() + timedelta(days=90), #3 months
        copy=False
    )
    facades = fields.Integer()
    garage = fields.Boolean()
    bedrooms = fields.Integer(string="Bedrooms", default=2)    
    active = fields.Boolean(string="Active", default=True)
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float() 
    living_area=fields.Integer()
    # State Field with Selection
    state = fields.Selection([
        ('new', "New"),
        ('offer_received', "Offer Received"),
        ('offer_accepted', "Offer Accepted"),
        ('sold', "Sold"),
        ('cancelled', "Cancelled"),
    ], string="State", required=True, default='new', copy=False, tracking=True)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
    ]

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.orientation = 'north'
        else:
            self.garden_area = 0
            self.orientation = False

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.ondelete(at_uninstall=False)
    def _check_property_deletion(self):
        for property in self:
            if property.state not in ['new', 'cancelled']:
                raise exceptions.UserError("You can only delete properties that are 'New' or 'Cancelled'.")
    
    def _track_subtype(self, init_values):
        """Trigger a notification when property is sold"""
        self.ensure_one()
        if 'state' in init_values and self.state == 'sold':
            return self.env.ref('estate.mt_property_sold')
        return super(EstateProperty, self)._track_subtype(init_values)

    # def action_cancel(self):
    #     # Cancels the property and prevents selling it later.
    #     for record in self:
    #         if record.state == 'sold':
    #             raise UserError("A sold property cannot be canceled.")
    #         record.state = 'cancelled'

    # def action_sold(self):
    #     # Marks the property as sold and prevents canceling it later.
    #     for record in self:
    #         if record.state == 'cancelled':
    #             raise UserError("Canceled properties cannot be sold.")
    #         record.state = 'sold'

    ## we can use above loop method in list view , when we are dealing with multiple records, like if 
    ## we want to sold or cancelled multiple properties at one time then we can use this.

    def action_cancel(self):
        # Cancels the property and prevents selling it later.        
        if self.state == 'sold':
            raise UserError("A sold property cannot be canceled.")
        self.state = 'cancelled'
        return True

    def action_sold(self):
        # Marks the property as sold and prevents canceling it later.        
        if self.state == 'cancelled':
            raise UserError("Canceled properties cannot be sold.")
        self.state = 'sold'
        return True
    
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.01):  # Ignore if selling price is 0
                min_acceptable_price = record.expected_price * 0.9
                if float_compare(record.selling_price, min_acceptable_price, precision_rounding=0.01) == -1:
                    raise models.ValidationError(
                        "Selling price cannot be lower than 90% of the expected price!"
                    )
