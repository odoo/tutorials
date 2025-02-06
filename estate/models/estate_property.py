from odoo import models,fields 
from datetime import date,timedelta

class EstateProperty(models.Model):
	_name="estate.property"
	_description = "Real Estate Property"

	name =fields.Char('Property Name',required =True)
	title=fields.Char('Title')
	description = fields.Text('Description')
	postcode=fields.Char('Postcode')
	available_from=fields.Date('Available From',copy=False,default=date.today()+timedelta(days=90))
	expected_price=fields.Float('Expected Price',required =True)
	selling_price = fields.Float('Selling Price',readonly=True,copy=False)
	bedrooms=fields.Integer('Bedrooms',default=2)
	living_area=fields.Integer('Living Area(sqm)')
	facades=fields.Integer('Facades')
	garage=fields.Boolean('Garage')
	garden=fields.Boolean('Garden')
	garden_area=fields.Integer('Garden Area')
	garden_orientation=fields.Selection([
		('north','North'),
		('south','South'),
		('east','East'),
		('west','West')
	],string="Garden Orientation",default='north')
	state=fields.Selection([
		('new','New'),
		('offer received','Offer Received'),
		('offer accepted','Offer Accepted'),
		('sold','Sold'),
		('cancelled','Cancelled')
	],string="Status",required=True,copy=False,default="new")
	active=fields.Boolean(string="Active",default=True)
	
	