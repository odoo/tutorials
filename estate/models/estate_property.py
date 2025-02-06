from odoo import api, models, fields
from datetime import timedelta

class EstateProperty(models.Model):
  _name = 'estate.property'
  _description = 'this is estate property Database model created by meem (meet moradiya)...'

  name = fields.Char('Property Name', required=True)
  description = fields.Text('Description')
  postcode = fields.Char('Postcode')
  date_avaibility = fields.Date('Date Avaibility', copy=False, default = lambda self: fields.Datetime.today() + timedelta(days = 90))
  expected_price = fields.Float('Expected Price', required=True)
  selling_price = fields.Float('Selling Price', readonly=True, copy=False)
  bedrooms = fields.Integer('Bedrooms', default=2)
  living_area = fields.Integer('Living Area')
  facades = fields.Integer('Facades')
  garage = fields.Boolean('Garage')
  garden = fields.Boolean('Garden')
  garden_area = fields.Integer('Garden Area')
  garden_orientation = fields.Selection(
    string='Orientation',
    selection=[
      ('north', 'North'), 
      ('south', 'South'), 
      ('east', 'East'), 
      ('west', 'West')
    ]
  )
  active = fields.Boolean('Active', default=True)
  state = fields.Selection(
    required=True,
    copy=False,
    default='new',
    string='state',
    selection=[
      ('new', 'New'), 
      ('offer received', 'Offer Received'), 
      ('offer accepted', 'Offer Accepted'), 
      ('sold', 'Sold'), 
      ('cancelled', 'Cancelled')
    ]
  )
  property_type_id = fields.Many2one('estate.property.type', 'Property Type')
  buyer = fields.Many2one('res.partner', 'Buyer', copy=False)
  sales_person = fields.Many2one('res.users', 'Salesperson', default=lambda self: self.env.user)
  tag_ids = fields.Many2many('estate.property.tag', 'Tags')
  offer_ids = fields.One2many('estate.property.offer', 'property_id', 'Offer')
  total_area = fields.Float('Total Area', compute='_compute_area')
  best_price = fields.Float('Best Price', compute='_compute_best_price')





########## Compute Mehods ##########

  @api.depends('living_area', 'garden_area')
  def _compute_area(self):
    for record in self:
      record.total_area = record.living_area + record.garden_area

  @api.depends('offer_ids.price')
  def _compute_best_price(self):
    for record in self:
      record.best_price = max(record.offer_ids.mapped('price'), default=0)
