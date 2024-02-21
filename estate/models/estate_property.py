from odoo import models, fields
from datetime import datetime, timedelta


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate property model"

    name = fields.Char(string='Name',
                       required=True,
                       help='This is the name of the estate property.',
                       index=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=datetime.today() + timedelta(days=3*30),
        copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default='new',
        selection=[
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ])

    property_type_id = fields.Many2one("estate.property.type", string="Type")

    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False)

    property_tag_ids = fields.Many2many("estate.property.tag")
