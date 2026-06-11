from dateutil.relativedelta import relativedelta

from odoo import api, fields, models # pylint: disable=import-error
from odoo.exceptions import UserError # pylint: disable=import-error
from odoo.exceptions import ValidationError # pylint: disable=import-error

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: (
            # Without lambda, date would be fixed permanently
            fields.Date.today() + relativedelta(months=3)
        )
    )
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    total_area = fields.Integer(
        compute='_compute_total'
    )
    best_offer = fields.Float(
        string='Best Offer',
        compute='_compute_best_offer'
    )
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        required=True,
        copy=False,
        default='new'
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
    )
    salesperson_id = fields.Many2one(
        "res.users",
        string="salesperson",
        default=lambda self: self.env.user,
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )
    tag_ids = fields.Many2many(
        "estate.property.tag",
        string="Tags",
    )
    offer_ids = fields.One2many(
        "estate.property.offer",
        "property_id",
        string="Offer",
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    _check_expected_price = models.Constraint(
        'CHECK(expected_price>0)',
        'Expected price must be strictly positive'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price>0)',
        'Selling price must be positive'
    )

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled Property cannot be sold")
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold Property cannot be canceled")
            record.state = "canceled"
        return True

