from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class Property(models.Model):
    _name = "estate.property"
    _description = "Property"

    name = fields.Char('Name', required=True)
    expected_price = fields.Float('Expected Price', digits=(12, 2), required=True)
    description = fields.Char('Description')
    date_availability = fields.Date('Available From', default=datetime.today() + relativedelta(months=+3), copy=False)
    selling_price = fields.Float('Selling Price', digits=(12, 2), readonly=True, copy=False)
    postcode = fields.Char('Postcode')
    bedrooms = fields.Integer('Bedrooms', default=2)
    facades = fields.Integer('Facades')
    living_area = fields.Integer('Living area')
    garden_area = fields.Integer('Garden area')
    total_area = fields.Integer(string='Total Area', compute='_compute_total', store=True)
    garden_orientation = fields.Selection(string='Orientation', selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
    garage = fields.Boolean('Has a Garage', default=False)
    garden = fields.Boolean('Has a Garden', default=False)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("canceled", "Cancelled")],
        required=True,
        default="new",
        copy=False
    )
    best_price = fields.Float('Best Offer', digits=(12, 2), compute='_compute_best_price', store=True)
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", index=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")

    _check_living_area = models.Constraint(
        "CHECK(living_area >= 0)",
        "The living area surface has to be positive."
    )
    _check_garden_area = models.Constraint(
        "CHECK(garden_area >= 0)",
        "The garden area surface has to be positive."
    )
    _check_bedrooms = models.Constraint(
        "CHECK(bedrooms >= 0)",
        "The bedroom number has to be positive."
    )
    _check_facades = models.Constraint(
        "CHECK(facades >= 0)",
        "The facade number has to be positive."
    )

    @api.depends('garden_area', 'living_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False
