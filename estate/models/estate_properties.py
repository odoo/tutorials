import logging
from dateutil import relativedelta as rd

from odoo import fields, models, api


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
    best_price = fields.Integer(compute="_compute_best_price")
    buyer_id = fields.Many2one(comodel_name='res.partner', copy=False)
    date_availability = fields.Date(string="Availability Date", copy=False, default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3))
    description = fields.Text()
    expected_price = fields.Float(string="Expected Price", required=True)
    facades = fields.Integer()
    garage = fields.Boolean(string="Has Garage?", help="Does the proeprty have a garage?")
    garden = fields.Boolean(string="Has Garden?", help="Does the property have a garden?")
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ],
        help="Directional orientation of the garden of the property shown"
    )
    living_area = fields.Integer()
    name = fields.Char(string="Property Name", required=True)
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id')
    postcode = fields.Char()
    property_type_colour = fields.Selection(related="property_type_id.colour", readonly=False)
    property_type_id = fields.Many2one(comodel_name="estate.property.type")
    salesperson_id = fields.Many2one(comodel_name='res.partner', default=lambda self: self.env.user.partner_id)
    # salesperson = fields.Char(default=_get_salesperson)
    selling_price = fields.Float(readonly=True, copy=False)
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
    total_area = fields.Integer(compute="_compute_total_area")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        _logger.error(self)
        for property in self:
            # _logger.error(property._fields)
            # _logger.error(property)
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for property in self:
            # _logger.error(self.mapped('offer_ids.price'))
            offer_prices = self.mapped('offer_ids.price')
            property.best_price = max(offer_prices) if offer_prices else 0
