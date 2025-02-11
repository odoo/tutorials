from odoo import api, fields, models

class EstatePropertyType(models.Model):
  _name = 'estate.property.type'
  _description = 'this is estate property type Database model created by meem (meet moradiya)...'
  _order = 'name asc'

  name = fields.Char(string='Property Type', required=True)
  property_ids = fields.One2many('estate.property', inverse_name='property_type_id', readonly=True)
  sequence = fields.Integer(string='Sequence', default=1)
  offer_ids = fields.One2many('estate.property.offer', inverse_name='property_type_id')
  offer_count = fields.Integer(string='Offer Count', default=0, compute='_compute_offer_count')

########## Compute Methods ##########

  @api.depends('offer_ids')
  def _compute_offer_count(self):
    for record in self:
      record.offer_count = len(record.offer_ids)
