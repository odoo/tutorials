from odoo import fields, models, api, exceptions, tools
from dateutil.relativedelta import relativedelta


class estateProperty(models.Model):
    _name = "estate.property"
    _description = "Unreal estate moves a lot more than real one"
    _order = "id desc"
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From", copy=False, default=lambda self: fields.Datetime.now() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    best_price = fields.Float(compute="_compute_best_price")
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (m^2)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")])
    active = fields.Boolean(default=True)
    state = fields.Selection(selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")], default='new')
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    customer_id = fields.Many2one("res.partner", string="Customer", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price >= 0)", "Expected price must not be negative"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "Sale price must not be negative")  # Should not be necessary, as offers are already constrained, but it's safer to make sure.
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            temp_best_price = 0
            for i in range(len(record.offer_ids)):
                temp_best_price = max(record.offer_ids[i].price, temp_best_price)
            record.best_price = temp_best_price

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_property_cancel(self):
        for record in self:
            if record.state != "sold" and record.state != "cancelled":
                record.state = "cancelled"
            else:
                raise exceptions.UserError("Redundant stage change, not permitter")
        return True

    def action_property_sell(self):
        for record in self:
            if record.state != "sold" and record.state != "cancelled":
                record.state = "sold"
            else:
                raise exceptions.UserError("Redundant stage change, not permitter")
        return True

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if not tools.float_utils.float_is_zero(record.selling_price, precision_digits=10) and tools.float_utils.float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=10) == -1:
                raise exceptions.UserError("The selling price must be at least 90% of the expected price. Consult your supervisor.")
    
    @api.ondelete(at_uninstall=False)
    def _unlink_property_estate(self):
        for record in self:
            if not record.state in ["new","cancelled"]:
                raise exceptions.UserError("Only new and cancelled properties can be deleted.")
