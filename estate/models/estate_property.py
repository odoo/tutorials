from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_is_zero, float_compare


class EstatePropertyModel(models.Model):
    _name = 'estate.property'
    _description = "Estate Property Model"

    name = fields.Char(string="Title", required=True)
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
    property_tag_id = fields.Many2many(
        "estate.property.tag", string="Property Tag")
    description = fields.Text()
    postcode = fields.Char(string="Postal code")
    date_availability = fields.Date(string="Available From", copy=False,
                                    default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    buyer_id = fields.Many2one(comodel_name="res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one(comodel_name="res.users", string="Salesperson", default=lambda self: self.env.user)
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name="property_id", string="Offers")
    best_price = fields.Float(compute="_compute_best_offer_price")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string="No of Bedrooms", default=2.00)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Number of Facades")
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Integer(compute="_compute_total_area")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West'),
        ]
    )
    active = fields.Boolean(default=True)
    status = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled'),
        ],
        default='new', required=True, copy=False
    )

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The Expected Price must be strictly positive!'
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The Selling Price must be positive!'
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_expected_price_ratio(self):
        for record in self:
            if not float_is_zero(record.selling_price, 2) and \
                    float_compare(record.selling_price, record.expected_price * 0.90, 2) < 0:
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price!")

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_offer_price(self):
        for record in self:
            record.best_price = max(record.mapped('offer_ids.price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = self.garden_area if self.garden_area else 10
            self.garden_orientation = self.garden_orientation if self.garden_orientation else 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def sold_property(self):
        for record in self:
            if record.status == 'cancelled':
                raise UserError("Cancelled Property cannot be sold!")
            record.status = 'sold'

    def cancel_property(self):
        for record in self:
            if record.status == 'sold':
                raise UserError("Sold Property cannot be cancelled!")
            record.status = 'cancelled'
