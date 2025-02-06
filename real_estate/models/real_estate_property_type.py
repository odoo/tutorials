from odoo import fields, models

class PropertiesType(models.Model):
	_name = 'real.estate.property.type'
	_description = "Real Estate Property Type Table"

	name = fields.Char("Property Type", required=True)
