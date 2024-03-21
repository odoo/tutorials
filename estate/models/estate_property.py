from odoo import api, exceptions, fields, models
from odoo.tools import float_utils


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate property"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available from",
                                    default=lambda _: fields.Date().add(fields.Date().today(), months=3), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(string="Garden Orientation",
                                          selection=[("north", "North"), ("south", "South"),
                                                     ("east", "East"), ("west", "West")])
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(string="State", default="new", copy=False, required=True,
                             selection=[("new", "New"), ("offer received", "Offer Received"),
                                        ("offer accepted", "Offer Accepted"), ("sold", "Sold"),
                                        ("canceled", "Canceled")])
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer", index=True, copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", index=True, default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offer")
    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The selling price must be positive")
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for estate in self:
            estate.total_area = estate.living_area + estate.garden_area

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for estate in self:
            estate.best_price = max(estate.offer_ids.mapped("price")) if estate.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_property_sold(self):
        if self.state == "canceled":
            raise exceptions.UserError("Canceled properties can't be sold")
        else:
            self.state = "sold"
        return True

    def action_property_canceled(self):
        if self.state == "sold":
            raise exceptions.UserError("Sold properties can't be canceled")
        else:
            self.state = "canceled"
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for estate in self:
            if (not float_utils.float_is_zero(estate.selling_price, 2) and
                    float_utils.float_compare(estate.selling_price, 0.9 * estate.expected_price, 2) < 0):
                raise exceptions.ValidationError("The selling price can't be lower than 90% of the expected price.")
