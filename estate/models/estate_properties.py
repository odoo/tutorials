import logging
from dateutil import relativedelta as rd

from odoo import fields, models


_logger = logging.getLogger(__name__)


def _get_availability_date(self):
    # _logger.info("!!! %s", self)
    return fields.Date.today() + rd.relativedelta(months=3)

def _get_salesperson(self):
    # _logger.info(self.env.user.name)
    # _logger.info(self.env.user.id)
    # _logger.info(self.env.user)
    return self.env.user


class EstateProperties(models.Model):
    _name = 'estate.properties'
    _description = 'Real Estate Properties'

    active = fields.Boolean(help="Should the property be listed?")
    bedrooms = fields.Integer(default=2)
    buyer_id = fields.Many2one(comodel_name='res.partner', copy=False)
    date_availability = fields.Date(string="Availability Date", copy=False, default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3))
    description = fields.Text()
    expected_price = fields.Float(string="Expected Price", required=True)
    facades = fields.Integer()
    garage = fields.Boolean(string="Has Garage?", help="Does the proeprty have a garage?")
    garden = fields.Boolean(string="Has Garden?", help="Does the property have a garden?")
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ],
        help="Directional orientation of the garden of the property shown"
    )
    living_area = fields.Integer(string="Living Area")
    name = fields.Char(string="Property Name", required=True)
    postcode = fields.Char()
    property_type_colour = fields.Selection(string="Type Colour", related="property_type_id.colour", readonly=False)
    property_type_id = fields.Many2one(string="Property Type", comodel_name="estate.property.type")
    salesperson_id = fields.Many2one(comodel_name='res.partner', default=lambda self: self.env.user.partner_id)
    # salesperson = fields.Char(default=_get_salesperson)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled")
        ],
        required=True, default='new', copy=False, string="Status"
    )
    tag_ids = fields.Many2many(comodel_name='estate.property.tag')
