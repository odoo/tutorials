from odoo import api, fields, models, exceptions
from odoo.tools.float_utils import float_compare, float_is_zero


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate properties"
    _order = "id desc"

    name = fields.Char("Title", required=True, )
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available From", copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection([
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West"),
        ], "Garden Orientation")
    status = fields.Selection([
        ("new", "New"),
        ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("cancelled", "Cancelled"),
        ], default="new", string="Status", required=True, copy=False)
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tags_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    best_offer = fields.Float("Best Offer", compute="_compute_best_offer")

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0.0)",
         "The expected price should be strictly positive."),
        ("check_selling_price", "CHECK(selling_price >= 0.0)",
         "The selling price should be positive.")
    ]

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for property in self:
            if float_is_zero(property.selling_price, precision_digits=2):
                return
            if float_compare(property.expected_price * 0.9, property.selling_price, precision_digits=2) > 0:
                raise exceptions.ValidationError("The selling price cannot be lower than 90% of the expected price")

    @api.constrains("expected_price")
    def _check_expected_price(self):
        for property in self:
            if float_is_zero(property.selling_price, precision_digits=2):
                return
            if float_compare(property.expected_price * 0.9, property.selling_price, precision_digits=2) > 0:
                raise exceptions.ValidationError("The selling price cannot be lower than 90% of the expected price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped("price") + [0.0])

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    def cancel_property(self):
        if self.filtered(lambda property: property.status == "sold"):
            raise exceptions.UserError("Sold properties cannot be cancelled")
        self.status = "cancelled"
        return True

    def sold_property(self):
        if self.filtered(lambda property: property.status == "cancelled"):
            raise exceptions.UserError("Cancelled properties cannot be sold")
        self.status = "sold"
        return True
