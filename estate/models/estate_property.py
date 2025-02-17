from odoo import fields, models
import datetime
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "this is the estate property model"
    name = fields.Char('Title', required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date('Available From', default=datetime.date.today() + relativedelta(months=5), copy=False)
    expected_price = fields.Float(digits=(20, 2), required=True)
    selling_price = fields.Float(digits=(20, 2), readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer('Garden Area (sqm)')
    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')])
    state = fields.Selection(selection=[
        ('new', 'New'),
        ('offer', 'Offer'),
        ('received', 'Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ], copy=False, required=True, default='new')
    active = fields.Boolean(default=True)

    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', copy=False, string='Buyer')
    salesman_id = fields.Many2one('res.users', default=lambda self: self.env.user, string='Salesman')
    tag_ids = fields.Many2many('estate.property.tag', string='Tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    _sql_constraints = []
