from odoo import models, fields
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):

    _name = "estate.property"
    _description = "Estate property"

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date Availability', copy=False, default=(
        date.today() + relativedelta(months=3)))
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', readonly=True)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area ')
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[
                                              ('north', 'North'),
                                              ('south', "South"),
                                              ('east', 'East'),
                                              ('west', 'West'),
                                          ]
                                          )
    active = fields.Boolean(string='Active', default=False)
    state = fields.Selection(string='Status',
                             selection=[
                                 ('new', 'New'),
                                 ('offer received', 'Offer Received'),
                                 ('offer accepted', 'Offer Accepted'),
                                 ('sold', 'Sold'),
                                 ('cancelled', 'Cancelled')
                             ]
                             )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type", string="Property Type")
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Buyer", copy=False)
    user_id = fields.Many2one(
        comodel_name="res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag", string="Tages")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers")
