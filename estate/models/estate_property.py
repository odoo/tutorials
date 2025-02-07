# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Contains all properties related to estate model"
    _order = "id desc"

    # Basic Details
    name = fields.Char(string="Title", required=True)
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Available From", copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3)
    )
    tag_ids = fields.Many2many(
        string="Property Tags", comodel_name="estate.property.tag"
    )
    property_type_id = fields.Many2one(
        string="Property Type", comodel_name="estate.property.type"
    )
    offer_ids = fields.One2many(
        string="Offers", comodel_name="estate.property.offer", inverse_name="property_id"
    )
    expected_price = fields.Float(string="Expected Price", required=True)
    selling_price = fields.Float(
        string="Selling Price", readonly=True, copy=False
    )

    # Description Fields
    description = fields.Text(string="Description")
    bedrooms = fields.Integer(string="Bedrooms", default=2)
    facades = fields.Integer(string="Facades")
    living_area = fields.Integer(string="Living Area (sqm)")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West")
        ]
    )
    total_area = fields.Integer(
        string="Total Area (sqm)", compute="_compute_total_area"
    )
    best_price = fields.Float(
        string="Best Price", compute="_compute_best_price")

    # Other Info
    buyer_id = fields.Many2one(string="Buyer", comodel_name="res.partner")
    salesperson_id = fields.Many2one(
        string="Salesperson",
        comodel_name="res.users",
        default=lambda self: self.env.user
    )

    # Reserved Fields Override
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        required=True,
        default="new"
    )
    active = fields.Boolean(default=True)

    _sql_constraints = [('check_expected_price', 'CHECK(expected_price > 0)',
                         'Expected price must be strictly positive'),
                        ('check_selling_price', 'CHECK(selling_price >= 0)',
                         'Selling price must be positive')]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            is_offer_accepted = any([offer.status == 'accepted' for offer in record.offer_ids])
            if is_offer_accepted and fields.float_compare(record.selling_price, 0.9 * record.expected_price, 2) == -1:
                raise ValidationError('Selling price must be atleast 90% of the expected price')

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max([x.price for x in record.offer_ids], default=0)

            # set state to offer received if offers are made
            if len(record.offer_ids) > 0 and record.state == 'new':
                record.state = 'offer_received'

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = "north"
            else:
                record.garden_area = 0
                record.garden_orientation = None

    def action_sell_property(self):
        if self.state == "cancelled":
            raise UserError('Cancelled property cannot be sold')

        self.state = "sold"

    def action_cancel_property(self):
        if self.state == "sold":
            raise UserError('Sold property cannot be cancelled')

        self.state = "cancelled"
