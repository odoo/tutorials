from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare

class EstateProperty(models.Model):
  _name = 'estate.property'
  _description = 'this is estate property Database model created by meem (meet moradiya)...'

  name = fields.Char(string='Property Name', required=True)
  description = fields.Text(string='Description')
  postcode = fields.Char(string='Postcode')
  date_avaibility = fields.Date(string='Date Avaibility', copy=False, default=lambda self: fields.Datetime.today() + timedelta(days = 90))
  expected_price = fields.Float(string='Expected Price', required=True)
  selling_price = fields.Float(string='Selling Price', readonly=True, copy=False)
  bedrooms = fields.Integer(string='Bedrooms', default=2)
  living_area = fields.Integer(string='Living Area')
  facades = fields.Integer(string='Facades')
  garage = fields.Boolean(string='Garage')
  garden = fields.Boolean(string='Garden')
  garden_area = fields.Integer(string='Garden Area')
  garden_orientation = fields.Selection(
    string='Garden Orientation',
    selection=[
      ('north', 'North'), 
      ('south', 'South'), 
      ('east', 'East'), 
      ('west', 'West')
    ]
  )
  active = fields.Boolean(string='Active', default=True)
  state = fields.Selection(
    string='Status',
    required=True,
    default='new',
    copy=False,
    selection=[
      ('new', 'New'), 
      ('offer received', 'Offer Received'), 
      ('offer accepted', 'Offer Accepted'), 
      ('sold', 'Sold'), 
      ('cancelled', 'Cancelled')
    ]
  )
  property_type_id = fields.Many2one('estate.property.type', string='Property Type')
  buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
  sales_person = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
  tag_ids = fields.Many2many('estate.property.tag', string='Tags')
  offer_ids = fields.One2many('estate.property.offer', inverse_name='property_id')
  total_area = fields.Float(string='Total Area', compute='_compute_area')
  best_price = fields.Float(string='Best Price', compute='_compute_best_price')

########## Compute, onchange and ondelete Methods ##########

  @api.depends('living_area', 'garden_area')
  def _compute_area(self):
    for record in self:
      record.total_area = record.living_area + record.garden_area

  @api.depends('offer_ids.price')
  def _compute_best_price(self):
    for record in self:
      record.best_price = max(record.offer_ids.mapped('price'), default=0)

  @api.onchange('garden')
  def _onchange_garden(self):
    if self.garden == True:
      self.garden_area = 10
      self.garden_orientation = 'north'
    else:
      self.garden_area = 0
      self.garden_orientation = ''

  @api.ondelete(at_uninstall=False)
  def _unlink_except_new_or_cancelled(self):
    for record in self:
      if record.state not in ['new', 'cancelled']:
        raise UserError(f"Cannot delete property '{record.name}' because its state is '{record.state}'. Only properties in 'New' or 'Cancelled' state can be deleted.")

########## Normal Methods ##########

  def action_set_property_sold(self):
    if self.state == 'cancelled':
      raise UserError('Cancelled properties cannot be Sold.')
    else:
      self.state = 'sold'
  
  def action_set_property_cancel(self):
    if self.state == 'sold':
      raise UserError('Sold properties cannot be cancelled.')
    else:
      self.state = 'cancelled'

########## SQL constraints ##########

  _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price >= 0.00)',
         'The Expected price must be Positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0.00)',
         'The Selling price must be Positive.')
    ]  
  
########## Python constraints ##########

  @api.constrains('selling_price', 'expected_price')
  def _check_selling_price(self):
    for record in self:
      if record.selling_price == 0.00:
        continue
      elif float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) == -1:
        raise ValidationError(f"Selling price cannot be lower than 90% of the expected price.")
