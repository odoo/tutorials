from odoo import api, fields, models, exceptions, tools


class Property(models.Model):
    _name = "estate.property"
    _description = "Real Estate property"
    _order = "sequence, id desc"

    sequence = fields.Integer("Sequence", default=1)
    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Available Date", copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float("Expected price", required=True)
    selling_price = fields.Float("Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden area (sqm)")
    garden_orientation = fields.Selection([
        ("north", "North"),
        ("south", "South"),
        ("east", "East"),
        ("west", "West")
    ], string="Garden Orientation")
    active = fields.Boolean("Active", default=True)
    state = fields.Selection([
        ("new", "New"),
        ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("canceled", "Canceled")
    ], string="Status", required=True, copy=False, default="new")

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)",
         "Expected price must be strictly positive."),
        ("check_selling_price", "CHECK(selling_price >= 0)",
         "Selling Price must be positive.")
    ]

    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type")
    salesman_id = fields.Many2one(
        "res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        "estate.property.offer", "property_id", string="Offers")

    total_area = fields.Float("Total area (sqm)", compute="_compute_area")
    best_price = fields.Float("Best price", compute="_compute_best_price")
    
    @api.depends("living_area", "garden_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max([0]+record.offer_ids.mapped('price'))

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_set_sold(self):
        for record in self:
            if record.state != "canceled":
                record.state = "sold"
            else:
                raise exceptions.UserError(
                    "Canceled properties cannot be sold.")

    def action_set_canceled(self):
        for record in self:
            if record.state != "sold":
                record.state = "canceled"
            else:
                raise exceptions.UserError(
                    "Sold properties cannot be canceled.")

    @api.constrains("expected_price", "selling_price")
    def _check_price(self):
        for record in self:
            if record.selling_price and record.expected_price and not tools.float_utils.float_is_zero(record.selling_price, precision_digits=2):
                if record.selling_price < 0.9 * record.expected_price:
                    raise exceptions.ValidationError(
                        "The selling price cannot be lower than 90% of the expected price.")
                

    @api.ondelete(at_uninstall=False)
    def _not_delete_if_not_new_or_canceled(self):
        for record in self:
            if record.state not in ["new", "canceled"]:
                raise exceptions.UserError(
                    "You cannot delete a property that is not new.")
