from odoo import models, fields
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(string="Title", required=True)
    Property_Type = fields.Text()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, readonly=True, default=lambda self: date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (m2)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (m2)')
    garden_orientation = fields.Selection(
        string='garden_orientation',
        selection=[('north', 'North'), ('south', 'South'),
        ('east', 'East'), ('west', 'West')])
    active = fields.Boolean(default=True)
    status = fields.Selection(copy=False, readonly=True, default='new',
        string='status',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
    )
    Property_Type_id = fields.Many2one('estate.property.type', string='Type')
    Buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    Salesman_id = fields.Many2one('res.users', string='Salesman', default=lambda self:self.env.user)
    tags_ids = fields.Many2many('estate.property.tags', string='Tags')
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="offer")
