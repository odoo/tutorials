from datetime import timedelta
from odoo import fields,models


class EstateProperty(models.Model):
    _name="estate.property"
    _description="Estate Property"

    name = fields.Char(string="Title",required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Available from",copy=False,default = fields.Date.today() + timedelta(days=+90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area(sqm)")
    garden_orientation = fields.Selection([
            ('north','North'),
            ('south','South'),
            ('east','East'),
            ('west','West')
        ], string='Direction',)
    active = fields.Boolean(default=True)
    state = fields.Selection([
            ('new','New'),
            ('offer recieved','Offer Recieved'),
            ('offer accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled'),
        ], string="State", default='new', required=True, copy=False)
    property_type_id = fields.Many2one("res.partner", string="Property Type")
