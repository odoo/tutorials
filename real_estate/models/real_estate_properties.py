from datetime import date, timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class real_estate(models.Model):
    _name = 'real.estate'
    _description = 'Real Estate Property'

    name = fields.Char(default="Unknown", required=True)
    street_address = fields.Char()
    description = fields.Text()
    postcode = fields.Integer()
    date_availability = fields.Datetime(default=date.today() + timedelta(days=90))
    expected_price = fields.Float()
    selling_price = fields.Float(default=1000)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    bathrooms = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    active = fields.Boolean(default=True)
    tag_ids = fields.Many2many(
        "real.estate.tag", string="Tags"
    )
    offer_ids = fields.One2many(
        "real.estate.property.offer", "property_id", string="Offers"
    )
    total_area = fields.Float(compute="_compute_total", store=True)
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
        store=True
    )

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_if_garden_orientation(self):
        for record in self:
            if record.garden_orientation == 'north':
                raise UserError("Can't delete an active record!")
