from odoo import models, fields

class EstatePropertyType(models.Model):
  _name = 'estate.property.type'
  _description = 'this is estate property type Database model created by meem (meet moradiya)...'

  name = fields.Char('Property Type', required=True)
