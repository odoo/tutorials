from odoo import fields, models,api,exceptions
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError,UserError
from odoo.tools.float_utils import float_is_zero, float_compare

class Property_Plan(models.Model):
    _name = "estate.property"
    _description = "Custom model for real estate."
    _order = "id desc"
    _inherit = ["mail.thread"]
    
    name = fields.Char(required=True, string="Title",tracking=True)
    tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    #One2Many
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="OfferID")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type" )
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.today() + relativedelta(months=3) ,string="Available From")
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_price = fields.Float(string="Total Area", compute="_compute_total_area")
    best_price = fields.Float(string="Best Offer", compute="_compute_best_price", store=True)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[("north","North"), ("south","South"),("east","East"),("west","West")],
        help="Type is used for direction"
    )
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ],copy=False,default='new')
    company_id = fields.Integer(default=lambda self:self.env.user.company_id,required=True)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'Expected price must be strictly positive.'),
         ('check_selling_price', 'CHECK(selling_price >= 0)',
         'Selling price must be positive.')
    ]
    
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_price = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"),default=0)
   
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_rounding=0.01):  
                acceptable_price = record.expected_price * 0.9 
                if float_compare(record.selling_price,acceptable_price, precision_rounding=0.01) == -1:
                    raise ValidationError("Selling price cannot be lower than 90% of the expected price.")
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'  
        else:
            self.garden_area = 0
            self.garden_orientation = None
    
    def action_set_cancel(self):
            if(self.state == 'sold'):
                raise exceptions.UserError("Sold properties can't be canceled")
            else:
                self.state = 'cancelled'
            return True
    
    def action_set_sold(self):
            if(self.state == 'cancelled'):
                raise exceptions.UserError("Canceled properties can't be sold")
            else:
                self.state = 'sold'
            return True
    
    @api.ondelete(at_uninstall=False)
    def __unlink_except_new_cancelled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError("You can only delete properties in 'New' or 'Cancelled' state.")
