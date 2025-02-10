from odoo import models, fields

class EstatePropertyType(models.Model):
  _name = 'estate.property.type'
  _description = 'this is estate property type Database model created by meem (meet moradiya)...'
  _order = 'name asc'

  name = fields.Char('Property Type', required=True)
  property_ids = fields.One2many('estate.property', 'property_type_id', readonly=True)
  sequence = fields.Integer('Sequence', default=1)

