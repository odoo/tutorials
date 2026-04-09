import logging
from dateutil import relativedelta as rd
from odoo import fields, models


_logger = logging.getLogger(__name__)


def _get_availability_date(self):
    # _logger.info("!!! %s", self)
    return fields.Date.today() + rd.relativedelta(months=3)


class EstateProperties(models.Model):
    _name = 'estate.properties'
    _description = 'Real Estate Properties'

    name = fields.Char(string="Property Name", required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Availability Date", copy=False, default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3))
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area")
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
    active = fields.Boolean(help="Should the property be listed?")
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
