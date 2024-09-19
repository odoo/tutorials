from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_is_zero, float_compare
from odoo.exceptions import ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate property"
    _order = "id desc"

    active = fields.Boolean(default=True)
    name = fields.Char(required=True, string="Title")
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Date.today() + timedelta(days=90))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )
    state = fields.Selection(
        [("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("canceled", "Canceled")],
        default="new",
        required=True,
        copy = False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    _sql_constraints = [
        ('property_positive_expected_price', 'CHECK (expected_price > 0)', 'Expected price must be positive'),
        ('property_positive_selling_price', 'CHECK (selling_price >= 0)', 'Selling price must be positive'),
    ]

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for record in self:
            # selling_price < expected_price*0.9
            if not float_is_zero(record.selling_price, 2) and float_compare(record.selling_price, record.expected_price*0.9, 2) == -1:
                raise ValidationError('The selling price cannot be lower than 90% of the expected price.')

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_sold_property(self):
        for record in self:
            if record.state == "canceled":
                raise UserError("A canceled property cannot be sold")
            record.state = "sold"
        return True

    def action_cancel_property(self):
        for record in self:
            if record.state == "sold":
                raise UserError("A sold property cannot be canceled")
            record.state = "canceled"
        return True

