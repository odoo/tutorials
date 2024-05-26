from odoo import models ,fields
from datetime import timedelta


class EstateProperty(models.Model):
    _name='estate.estate_property'
    _description = 'Estate properties table'

    name= fields.Char(string='Property name',required=True,help='Name of the property')
    description = fields.Text(string='Description of proberty')
    postcode =fields.Char(string='Postcode',required=True , help='Postcode of the property')
    date_availability=fields.Date(string='Available date',help='Available date for the property',copy=False,default= fields.Date.today() +timedelta(days=90))
    expected_price=fields.Float(string='Expected Price',required=True ,help='Expected Price of the property')
    selling_price = fields.Float(string='Sell Price',required=True, help='Selling price',readonly=True )
    bedrooms = fields.Integer(string='Bedrooms',help='Number of bedrooms',default=2)
    living_area=fields.Integer(string='Living area count',help='Number of living areas')
    facades=fields.Integer(string='Facades', help='Number of facades')
    garage=fields.Boolean(string='Garage',help='Is garage availabe')
    garden= fields.Boolean(string='Garden',help='Is garage availabe')
    garden_area = fields.Integer(string='Garden Area', help='Garden are in square meters')
    garden_orientation = fields.Selection(
                                            string='Geographical orientation',
                                            selection=[('north', 'North'), ('south', 'South'),
                                                    ('east','East'),('west','West')],
                                            help="Type is used to specify geographical orientation")
