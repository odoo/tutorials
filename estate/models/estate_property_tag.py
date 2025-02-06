from odoo import models, fields

class EstatePropertyTag(models.Model):
  _name = 'estate.property.tag'
  _description = 'this is estate property tag Database model created by meem (meet moradiya)...'

  name = fields.Char('Property Tag', required=True)
