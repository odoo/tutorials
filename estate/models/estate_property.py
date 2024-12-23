from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    user_id = fields.Many2one("res.users", string="Salesperson", index=True, tracking=True, default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("PostCode")
    date_availability = fields.Date("Availability Date", copy=False)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    expected_price = fields.Float("Expected Price", required=True)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        "Garden Orientation",
    )
    state = fields.Selection(
        [("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
        default="new", group_expand=True)
    active = fields.Boolean("Active", default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tags", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")
    company_id = fields.Many2one(
        "res.company", string="Company", default=lambda self: self.env.company
    )
    _order = "id desc"

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price >= 0)", "A property expected price must be strictly positive"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "A property selling price must be positive"),
    ]
    

    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            # Only check when the offer is accepted
            if record.selling_price != 0:
                if record.selling_price < (0.9 * record.expected_price):
                    raise UserError(
                        "The selling price must be at least 90% of the expected price."
                    )

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if not record.offer_ids:
                record.best_price = 0
            else:
                record.best_price = max(record.offer_ids.mapped("price"))

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0

    @api.ondelete(at_uninstall=False)
    def _ondelete_property(self):
        for record in self:
            if record.state != "new" and record.state != "cancelled":
                raise UserError(
                    "You cannot delete a property that is not in New or Cancelled state."
                )

    def action_change_state(self):
        param_value = self.env.context.get("param_name", "default_value")

        for record in self:
            if param_value == "sold" and record.state == "cancelled":
                raise UserError(
                    "You cannot change the state of a cancelled property to sold."
                )
            if param_value == "cancelled" and record.state == "sold":
                raise UserError(
                    "You cannot change the state of a sold property to cancelled."
                )
            if param_value == "new":
                record.state = "new"
            elif param_value == "offer_received":
                record.state = "offer_received"
            elif param_value == "offer_accepted":
                record.state = "offer_accepted"
            elif param_value == "sold":
                record.state = "sold"
            elif param_value == "cancelled":
                record.state = "cancelled"

    def action_add_offer(self):
        active_ids = self.env.context.get("active_ids", [])
        return {
            "type": "ir.actions.act_window",
            "name": "Add Offer to Property",
            "res_model": "estate.property.offer.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_property_ids": active_ids},
        }
