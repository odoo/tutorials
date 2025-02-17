from odoo import api, exceptions, fields, models
from datetime import date, timedelta
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property" 
    _description = "Real Estate Property"
    _inherit = ['mail.thread']
    _order = "id desc" 

    name = fields.Char(string="Title", required=True , tracking=True)
    expected_price = fields.Float(string="Expected Price", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From",copy=False, default=lambda self: date.today() + timedelta(days=(90)))
    selling_price = fields.Float(string="Selling Price",readonly=True,copy=False)
    bedrooms = fields.Integer(string="Bedrooms",default=2)
    living_area = fields.Integer(string="Living Area")
    facades = fields.Integer(string="Facades")
    active = fields.Boolean(default=True)
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection([
        ('north', 'North'), ('south', 'South'),
        ('east', 'East'),('west', 'West')
        ],string="Garden Orientation")

    state = fields.Selection([
        ('new', 'New'),('offer_received','Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),('cancelled', 'Cancelled'),
        ],string="State",required=True,default='new',copy=False)
                    
    property_type_id = fields.Many2one("estate.property.type",string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False , tracking=True)
    salesperson_id = fields.Many2one("res.users",string="Salesman",default= False) 
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area",string="Total Area")
    best_offer = fields.Float(compute="_compute_best_offer", store=True)
    company_id = fields.Many2one("res.company", string="Company Id", default = lambda self:self.env.company, required=True)

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
        
    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped("price"), default=0.0)
  
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"

    def action_set_sold(self):
        for record in self:
            if  record.state != 'offer_accepted':
                raise exceptions.UserError("Accept an offer first!")
            if not record.offer_ids:
                raise exceptions.UserError("No offers available to accept!")
            record.state = "sold"
        return True

    def action_cancel_property(self):
        for record in self:
                record.state = "cancelled"
        return True

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)','The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, record.expected_price * 0.9,precision_digits=2) < 0:
                    raise ValidationError(f"The selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise exceptions.UserError("You can only delete properties in 'New' or 'Cancelled' state.")
