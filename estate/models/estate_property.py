from dateutil.relativedelta import relativedelta

from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "ESTATE property"

    currency_id = fields.Many2one(
        'res.currency',
        default=lambda self: self.env.company.currency_id, required=True)
    name = fields.Char(required=True)
    property_type = fields.Text("Description", required=True)
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Monetary(currency_field='currency_id', required=True)
    selling_price = fields.Monetary(currency_field='currency_id', readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Float()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Float()
    garden_orientation = fields.Selection([('n', 'N'), ('s', 'S'), ('w', 'W'), ('e', 'E')])
    active = fields.Boolean(default=True)
    status = fields.Selection([('_new', 'New'), ('offer_received', 'Offer received'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], default='_new', required=True)
