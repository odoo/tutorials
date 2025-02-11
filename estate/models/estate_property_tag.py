from odoo import fields, models

class EstatePropertyTag(models.Model):
  _name = 'estate.property.tag'
  _description = 'this is estate property tag Database model created by meem (meet moradiya)...'
  _order = 'name asc'

  name = fields.Char(string='Property Tag', required=True)
  color = fields.Integer(string='Color')

########## constraints ##########

  _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)',
         'Tag names must be unique.')
    ]  
  
  