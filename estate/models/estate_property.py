from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "Real-estate property"
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=fields.Date.add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        default='new',
        copy=False,
    )
    garden_orientation = fields.Selection(
        string="Type",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
    )
    property_type = fields.Many2one('estate.property.type', string="property type")
    salesman_id = fields.Many2one(
        'res.users', string="Salesman", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Float(compute='_compute_total_area', store=True)
    best_price = fields.Float(compute='_compute_best_price', store=True)
    _chek_expected_price = models.Constraint(
        "CHECK(expected_price > 0)", "Expected price of property should be positive"
    )
    _chek_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)", "selling price of property should be positive"
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchnage_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_property_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("cancelled property cannot be sold")
            else:
                record.state = 'sold'
        return True

    def action_property_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("sold property cannot be cancelled")
            else:
                record.state = 'cancelled'
        return True

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if (
                record.selling_price
                and float_compare(
                    record.selling_price,
                    record.expected_price * 0.9,
                    precision_digits=2,
                )
                == -1
            ):
                raise ValidationError(
                    "Selling price should not be less than 90% of expected price"
                )
