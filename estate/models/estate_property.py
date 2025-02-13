from odoo import fields,api,models
from datetime import datetime, timedelta
from odoo.exceptions import UserError,ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Estate Model"

    name = fields.Char(required=True)
    id = fields.Integer(required=True)
    create_uid = fields.Integer()
    create_date = fields.Date()
    write_uid = fields.Integer()
    write_date = fields.Date()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From" , copy = False , default= datetime.now() + timedelta(days=90))
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True , copy = False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ])
    state = fields.Selection([
        ('new', 'NEW'),
        ('offer_received', 'OFFER RECIEVED'),
        ( 'offer_accepted', 'OFFER ACCEPTED'),
        ('sold' , 'SOLD'),
        ('canceled' , 'CANCELED')],
        required = True, default = "new", copy = False)
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type" ,string="Property Type")
    buyer_id = fields.Many2one("res.partner",string="Buyer" , copy=False)
    user_id = fields.Many2one("res.users", string="Salesperson" , default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string='Tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float(compute='_compute_total_area')
    _order = 'id desc'
    best_price = fields.Float(compute="_compute_best_price", store=True)
    company_id= fields.Many2one(comodel_name="res.company", string="related company", required=True, default=lambda self: self.env.user.company_id)

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive'),
    ]   

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
             record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0
   
    @api.onchange('garden')
    def garden_value_change(self):
        if(self.garden):
            self.garden_area=10
            self.garden_orientation='north' 
        else:
            self.garden_area=0
            self.garden_orientation=None

    @api.constrains('expected_price', 'selling_price')
    def _check_price(self):
        for record in self:
          if not float_is_zero(record.selling_price, precision_digits=2):
              if(float_compare(record.selling_price , record.expected_price * 0.9 , precision_digits=2) < 0):
                  raise ValidationError("The selling price cannot be lower than 90% of the expected price")
    
    @api.ondelete(at_uninstall=False)
    def _unlink_if_not_new_or_cancelled(self):
        for record in self:
            if record.state not in ('new', 'canceled'):
                raise UserError(("You may only delete properties in state 'New' or 'Cancelled'"))

                
    def action_property_sold(self):
        if self.state not in ('offer_accepted'):
            raise ValidationError("Offer should be accepted before selling the property")
        for record in self:
            if(record.state == 'cancelled'):
                raise UserError(("Cancelled property cannot be sold."))
            record.state='sold'
        return True
    
    def action_property_cancel(self):
        for record in self:
            if(record.state == "sold"):
                raise UserError(("Sold property cannot be canceled."))
            record.state="canceled" 
        return True
