# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Land, Office or any property details for Real Estate module"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char('PostCode')
    date_availability = fields.Date('Available From', copy=False, default=lambda self: fields.Date.today(self) + relativedelta(months=3))  # in 3 months
    expected_price = fields.Float('Expected Price', required=True)
    selling_price = fields.Float('Selling Price', copy=False, readonly=True)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Total Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
    )
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        readonly=True,
        copy=False,
        default='new',
    )
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    salesman = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    active = fields.Boolean('Active', default=True)

    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'))

    @api.onchange("garden")
    def _onchange_garden(self):
        if (self.garden):
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False

    def action_cancel(self):
        for record in self:
            if (record.state != 'sold'):
                record.state = 'cancelled'
            else:
                raise exceptions.ValidationError("Sold property cannot be cancelled")
        return True

    def action_sold(self):
        for record in self:
            if (record.state != 'cancelled'):
                record.state = 'sold'
            else:
                raise exceptions.ValidationError("Cancelled property cannot be sold")
        return True
