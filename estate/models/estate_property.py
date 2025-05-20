from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'estate property module'

    name = fields.Char(required=True)
    description = fields.Text("Description")
    date_availability = fields.Date(
        "Date Availability", default=fields.Date.today() + relativedelta(months=3), copy=False
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", default=0, readonly=True, copy=False)
    bedrooms = fields.Integer(required=True, default=2)
    living_area = fields.Integer("Living Area (sqm)", required=True)
    facades = fields.Integer(default=0)
    garage = fields.Boolean(default=False)
    garden = fields.Boolean(default=False)
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('east', 'East'), ('south', 'South'), ('west', 'West')]
    )
    total_area = fields.Integer("Total Area (sqm)")
    postcode = fields.Integer()
    active = fields.Boolean(default=True)
    status = fields.Selection(
        [
            ('new', 'New'),
            ('offer received', 'Offer Received'),
            ('offer accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new',
        copy=False,
    )
    partner_type_id = fields.Many2one(comodel_name="estate.property.type")
    buyer_id = fields.Many2one(comodel_name="res.partner")
    user_id = fields.Many2one(comodel_name="res.users", default=lambda self: self.env.user)
