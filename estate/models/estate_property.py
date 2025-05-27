
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Properties of the estate model"
    _order = "id desc"

    active = fields.Boolean(default=True)
    name = fields.Char("Title", required=True)
    description = fields.Text("description")
    postcode = fields.Integer("Post code")
    date_availability = fields.Date(
        "Date availability",
        copy=False,
        default=lambda S: fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float("Expected price", required=True)
    selling_price = fields.Float("Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer("# Bedrooms", default=2)
    living_area = fields.Integer("Living area")
    facades = fields.Integer("# facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden area", default=0)
    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[("north", "North"), ("east", "East"), ("west", "West"), ("south", "South")])
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")],
        required=True,
        copy=False,
        default="new")
    property_type_id = fields.Many2one("estate.property.type")
    buyer = fields.Many2one("res.partner", copy=False)
    salesperson = fields.Many2one("res.users", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id")
    total_area = fields.Float("Total Area", compute="_compute_area")
    best_price = fields.Float("Best Price", compute="_find_best_price")

    _sql_constraints = [
        ('positive_expecting_price', "CHECK(expected_price > 0)", "Property should have a strictly positive expected price !"),
        ("positive_sell_price", "CHECK(selling_price > 0)", "Property should have a strictly positive selling price !"),
        ]

    @api.depends("garden_area", "living_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _find_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_sold(self):
        for a_property in self:
            if a_property.state not in ["cancelled"]:
                a_property.state = "sold"
            else:
                raise UserError(self.env._("Property is already cancelled"))
        return True

    def action_cancel(self):
        for a_property in self:
            if a_property.state not in ["sold"]:
                a_property.state = "cancelled"
            else:
                raise UserError(self.env._("Property is already sold"))
        return True

    @api.constrains("selling_price")
    def _check_minimum_sell_price(self):
        for a_property in self:
            if float_compare(a_property.selling_price, a_property.expected_price * 0.9, 2) == -1:
                raise ValidationError("The selling price can not be lower than 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        if any(record.state not in ["new", "cancelled"] for record in self):
            raise UserError(self.env._("Property should be New or Cancelled in order to be deleted"))
