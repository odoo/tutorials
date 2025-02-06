# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models,fields 
from datetime import date,timedelta


class EstateProperty(models.Model):
	_name="estate.property"
	_description = "Real Estate Property"

	name =fields.Char(string='Property Name')
	title=fields.Char(string='Title')
	description = fields.Text(string='Description')
	postcode=fields.Char(string='Postcode')
	available_from=fields.Date(string='Available From',copy=False,default=date.today()+timedelta(days=90))
	expected_price=fields.Float(string='Expected Price',required =True)
	selling_price = fields.Float(string='Selling Price',readonly=True,copy=False)
	bedrooms=fields.Integer(string='Bedrooms',default=2)
	living_area=fields.Integer(string='Living Area(sqm)')
	facades=fields.Integer(string='Facades')
	garage=fields.Boolean(string='Garage')
	garden=fields.Boolean(string='Garden')
	garden_area=fields.Integer(string='Garden Area')
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
	property_type_id = fields.Many2one('estate.property.type', string="Property Type")
	buyer_id=fields.Many2one("res.partner",string="Buyer",copy=False)
	salesperson_id = fields.Many2one("res.users",string="Salesperson",default=lambda self: self.env.user)


