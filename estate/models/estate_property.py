from odoo import models,fields 

class EstateProperty(models.Model):
	_name="estate.property"
	_desciption = "Real Estate Property"

	name =fields.Char('Property Name',required =True)
	description = fields.Text('Description')
	expected_price=fields.Float('Expected Price',required =True)
	selling_price = fields.Float('Selling Price')
