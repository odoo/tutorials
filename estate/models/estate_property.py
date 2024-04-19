from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
class Property(models.Model):

    _name = "estate_property"
    _description = "The properties of the real estate property"
    _sql_constraints = [
        ('check_positive_expected_price', 'CHECK (expected_price > 0)', 'The expected price must be strictly postive'),
        ('check_positive_selling_price', 'CHECK (selling_price >= 0)', 'The selling price must be positive'),
    ]
    _order = 'id desc'
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    garden_area = fields.Integer()
    total_area = fields.Integer(compute="_compute_total_area")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_orientation = fields.Selection(
        selection=[
            ('North', 'North'),
            ('South', 'South'),
            ('East', 'East'),
            ('West', 'West'),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('New', 'New'),
            ('Offer Received', 'Offer Received'),
            ('Offer Accepted', 'Offer Accepted'),
            ('Sold', 'Sold'),
            ('Canceled', 'Canceled')
        ],
        required=True,
        copy=False,
        default='New',
    )
    property_type_id = fields.Many2one("estate_property_type", string="Property Type")
    user_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    partner_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_tag_ids = fields.Many2many("estate_property_tag")
    property_offer_ids = fields.One2many("estate_property_offer", "property_id", string="Offers")
    best_offer = fields.Float(compute="_compute_best_offer")
    PRECISION_ROUNDING = 1e-5
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("property_offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.mapped("property_offer_ids.price")) if record.property_offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "North"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_sold(self):

        if self.state == "Canceled":
            raise UserError("A canceled property cannot be sold")

        if "Accepted" not in self.mapped("property_offer_ids.status"):
            raise UserError("A property cannot be sold without accepted offers")

        self.state = "Sold"
        return True

    def action_cancel(self):

        if self.state == "Sold":
            raise UserError("A sold property cannot be canceled")

        self.state = "Canceled"
        return True

    @api.constrains('expected_price', 'selling_price')
    def check_selling_price(self):
        for estate_property in self:
            if (
                not float_is_zero(
                    estate_property.selling_price,
                    precision_rounding=self.PRECISION_ROUNDING,
                ) and
                float_compare(
                    estate_property.selling_price,
                    0.9 * estate_property.expected_price,
                    precision_rounding=self.PRECISION_ROUNDING,
                ) < 0
            ):
                raise ValidationError('The selling price cannot be less than 90% of the expected price')
