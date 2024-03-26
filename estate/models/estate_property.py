"""module for the estate property model"""

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.tools.translate import _


class EstateProperty(models.Model):
    "Estate property odoo model"
    _name = "estate.property"
    _description = "real estate assets"
    _order = "id desc"
    _sql_constraints = [
            ("positive_expected_price", "CHECK(expected_price > 0)", "expected price must be more than 0"),
            ("positive_selling_price", "CHECK(selling_price >= 0)", "selling price must be 0 or more")
            ]

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
            "Available From",
            default=lambda _: fields.Date.add(fields.Date.today(), months=3),
            required=True)
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price")
    bedrooms = fields.Integer("# bedrooms", default=2)
    living_area = fields.Integer("Living Area (m2)")
    facades = fields.Integer("# facades")
    garage = fields.Boolean("Has Garage")
    garden = fields.Boolean("Has Garden")
    garden_area = fields.Integer("Garden Area (m2)")
    garden_orientation = fields.Selection([("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")])
    active = fields.Boolean(default=True)
    state = fields.Selection(
            [("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("canceled", "Canceled")],
            required=True, default="new", string="Status", copy=False)
    type_id = fields.Many2one("estate.property.type", string="Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    best_price = fields.Float("Best Offer", compute="_compute_best_price")
    total_area = fields.Float("Total Area (m2)", compute="_compute_total_area", default=0.0)

    def action_set_sold(self):
        self.ensure_one()
        if self.state == "offer_accepted":
            return self.write({"state": "sold"})

        if self.state == "canceled":
            raise UserError(_("Sale was already canceled"))
        else:
            raise UserError(_("You need to accept an offer before setting a property as sold"))

    def action_cancel(self):
        self.ensure_one()
        if self.state != "sold":
            return self.write({"state": "canceled"})
        else:
            raise UserError(_("Already sold"))

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for rec in self:
            self.best_price = max(rec.offer_ids.mapped("price"), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for rec in self:
            if float_is_zero(rec.selling_price, precision_digits=2):
                continue
            if float_compare(rec.selling_price, 0.9 * rec.expected_price, precision_rounding=0.1) < 0:
                raise ValidationError(_("selling price must be above 90% of the expected price"))

    @api.ondelete(at_uninstall=False)
    def _constrain_delete(self):
        for rec in self:
            if rec.state not in ["new", "canceled"]:
                raise UserError(_("Can only delete when status is 'New' or 'Canceled'"))
