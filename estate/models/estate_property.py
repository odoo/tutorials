from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero



class estateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order="id desc"

    # Basic fields for property details
    name = fields.Char(string="Property name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Availability Date",
        default=lambda self: fields.Date.today() + relativedelta(months=3)  
    )
    
    # to add a buyer and seller field in our form beacuse of the buyer can be anyone one but the seller must be the employer or the seller owner
    buyer_id=fields.Many2one("res.partner", string="buyer" , required=False ,copy=False)
    salesperson_id=fields.Many2one("res.users", string="sales_person_name" , default= lambda self: self.env.user, required=True)

    expected_price = fields.Float(string="Expected Price", required=True, default=0.0)
    selling_price = fields.Float(string="Selling Price", readonly=True)  
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    living_area = fields.Integer(string="Living Area (sq.m.)")
    facades = fields.Integer(default=3)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Date Deadline")
    garage = fields.Boolean(string="Has Garage")
    garden = fields.Boolean(string="Has Garden")
    garden_area = fields.Integer(string="Garden Area (sq.m.)")
    garden_orientation = fields.Selection([
        ("north", "North"),
        ("south", "South"),
        ("new", "new"),
        ("offer received","offer received"),
        ("east", "East"),
        ("west", "West")
    ], string="Garden Orientation")

    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("not sold","not sold"),
            ("cancelled", "Cancelled")
        ],
        default="new",
        required=True,
        copy=False,
     )
    active = fields.Boolean(default=True)  

     #  to use a compute decorator
    living_area=fields.Float(string="living_area")
    garden_area=fields.Float(string="garden_area")
    total_area=fields.Float(string="total_area", compute="compute_total_area", store=True)

    @api.depends("living_area", "garden_area")
    def compute_total_area(self):
        for record in self:
            record.total_area=record.living_area+record.garden_area

   
    # we have add the many relation ship of model
    property_type_id = fields.Many2one("estate.property.type", string="Property Type" )
    tag_ids=fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price", store=True)

    #  we have to add the best price decorated to use to show the best price in our field
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            # Get the maximum price from all related offers using mapped
            best_offer = max(record.offer_ids.mapped("price"), default=0.0)
            record.best_price = best_offer



    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10  
            self.garden_orientation= "north"  
        else:
            self.garden_area = False  
            self.garden_orientation= False

    def action_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled.")
            record.state = "cancelled"
        return True

    def action_set_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold.")
            record.state = "sold"
        return True
    
    
    _sql_constraints = [
    ("check_expected_price", "CHECK(expected_price >= 0 OR expected_price IS NULL)", "The expected price must be strictly positive."),
    ("check_selling_price", "CHECK(selling_price >= 0 OR selling_price IS NULL)", "The selling price must be positive."),
    ]
    
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        """Ensures that the selling price is at least 90% of the expected price unless it is zero."""
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                min_price = record.expected_price * 0.9
                if float_compare(record.selling_price, min_price, precision_digits=2) == -1:
                    raise models.ValidationError( "The selling price cannot be lower than 90% of the expected price!")
                
    @api.ondelete(at_uninstall=False)
    def _unlink_if_allowed(self):
        """ Prevent deletion if property state is not 'New' or 'Cancelled'. """
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError("You can only delete properties that are in 'New' or 'Cancelled' state.")
