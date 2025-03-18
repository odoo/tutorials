from odoo import fields, models

class EstatePropertyTags(models.Model):
	_name = 'estate.property.tags'
	_description = 'estate property tag'
	
	name = fields.Char('Name', required=True)
