from odoo import models, fields
from datetime import timedelta

class EstateProperty(models.Model):
  _name = 'estate_property'
  _description = 'this is estate property Database model created by meem (meet moradiya)...'

  name = fields.Char(required=True)
  description = fields.Text()
  postcode = fields.Char()
  date_avaibility = fields.Date(copy=False, default = lambda self: fields.Datetime.today() + timedelta(days = 90))
  expected_price = fields.Float(required=True)
  selling_price = fields.Float(readonly=True, copy=False)
  bedrooms = fields.Integer(default=2)
  living_area = fields.Integer()
  facades = fields.Integer()
  garage = fields.Boolean()
  garden = fields.Boolean()
  garden_area = fields.Integer()
  garden_orientation = fields.Selection(
    string='Orientation',
    selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
  )
  active = fields.Boolean(default=True)
  state = fields.Selection(
    required=True,
    copy=False,
    default='new',
    string='state',
    selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')]
  )
