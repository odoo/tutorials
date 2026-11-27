from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _table = "estate_property"

    name = fields.Char(required=True)
    description = fields.Text()
    postal_code = fields.Char()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
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
            ('cancelled', 'Cancelled'),
        ],
        default='new', required=True, string="State", copy=False,
    )

    # Compute Fields
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_offer_price")

    # Relational Fields
    property_type_id = fields.Many2one("estate.property.type", "Property Type")
    buyer_id = fields.Many2one("res.partner", "Buyer", copy=False)
    salesperson_id = fields.Many2one(
        "res.users", "Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", "Offers")

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be positive !'
    )

    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'The selling price must be positive !'
    )

    @api.constrains("selling_price")
    def _check_minimum_selling_price_limit(self):
        for record in self:
            is_zero = float_is_zero(record.selling_price, 2)
            comparison_invalid = float_compare(
                record.selling_price, (record.expected_price * 0.9), 2) == -1
            if not is_zero and comparison_invalid:
                raise ValidationError(
                    "This selling price is too low to be allow !")

    # Compute Methods
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer_price(self):
        for record in self:
            record.best_price = max(
                record.offer_ids.mapped("price"), default=0.0)

    # Onchange Method
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10 if not self.garden_area else self.garden_area
            self.garden_orientation = 'north' if not self.garden_orientation else self.garden_orientation
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # Action Methods
    def action_set_property_status_sold(self):
        self.ensure_one()
        if self.state == "cancelled":
            raise UserError(
                "Cancelled Property Can't Be Move To Sold !")
        if self.state == "sold":
            raise UserError(
                "Property Is Already Sold !")
        else:
            self.state = "sold"
            return True

    def action_set_property_status_cancel(self):
        self.ensure_one()
        if self.state == "sold":
            raise UserError(
                "Sold Property Can't Be Move To Cancelled !")
        if self.state == "cancelled":
            raise UserError(
                "Property Is Already Cancelled !")
        else:
            self.state = "cancelled"
            return True
