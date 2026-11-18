# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property test model'
    _states = [
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
    ]

    def _get_availability_default():
        today = fields.Date.today()
        return fields.Date.add(today, months=3)

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=_get_availability_default())
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Char()
    active = fields.Boolean(default=False)
    state = fields.Selection(selection=_states, required=True, readonly=True, default='new')
    partner_id = fields.Many2one("res.partner", string="Partner")
    type_id = fields.Many2one("estate.property.type", string="Type")
