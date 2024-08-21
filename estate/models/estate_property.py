from odoo import models, fields

class EstateProperty(models.Model):
	_name = 'estate.property'
	_description = 'The Real Estate Advertisement module'

	name = fields.Char('Name', required=True)
	description = fields.Text('Description')
	postcode = fields.Char('Postcode')
	bedrooms = fields.Integer('Bedrooms', default=2)
	living_area = fields.Integer('Living Area (aqrm)')
	facades = fields.Integer('Fcadres')
	garage = fields.Boolean(default=False)
	garden = fields.Boolean(default=False)
	garden_area = fields.Integer('area', default=0)
	expected_price = fields.Float('Expected Price', required=True)
	active = fields.Boolean(default=True)

	date_availability = fields.Date(
		'Availability Date',
		copy=False,
		default=fields.Datetime.add(fields.Datetime.today(), months=3)
	)

	selling_price = fields.Float(
		'Selling Price',
		readonly=True,
		copy=False
		)
	
	garden_orientation = fields.Selection(
		[
            ('North', 'North'),
            ('South', 'South'),
            ('East', 'East'),
            ('West', 'West')
        ],
		string = 'Garden Orientation',
	)
	state = fields.Selection(
		[
			("New", "New"),
			("Offer Received", "Offer Received"),
			("Offer Accepted", "Offer Accepted"),
			("Sold", "Sold"),
			("Canceled", "Canceled")
		],
		default="New",
		required=True,
		copy=False
	)
