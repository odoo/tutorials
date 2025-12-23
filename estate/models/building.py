from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class Building(models.Model):
    _name = 'estate.building'
    _description = 'Buildings'
    _order = "id desc"

    name = fields.Char()
    description = fields.Text()
    value = fields.Integer(copy=False)
    availability_date = fields.Date(
        default=lambda self: fields.Date.today() + timedelta(days=90), copy=False
    )
    number_of_rooms = fields.Integer(default=2)
    garden_area = fields.Integer()
    building_area = fields.Integer()
    garden_orientation = fields.Selection(
        [("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")],
        "garden Orientation",
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
    )
    post_code = fields.Integer(default=1000)
    building_type_id = fields.Many2one("estate.building_type", string="Building Type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesperson_id = fields.Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many("estate.building_tags", string="Tags")
    offer_ids = fields.One2many("estate.offer", "building_id", string="Offers")

    total_area = fields.Integer(string="Total Area", compute="_compute_total_area")

    best_price = fields.Integer(
        string="Best Offer Price",
        compute="_compute_best_price",
    )
    has_garden = fields.Boolean(string="Has Garden", default=False)

    _price_constraint = models.Constraint(
        "CHECK (value > 0)", "Price must be POSITIVE."
    )
    _name_constraint = models.Constraint(
        "UNIQUE(name)", "Building name must be UNIQUE."
    )

    @api.depends("building_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.building_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    @api.onchange("has_garden")
    def _onchange_garden_area(self):
        if self.has_garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_set_sold(self):
        for record in self:
            if record.state == "canceled":
                raise UserError(self.env._("Canceled buildings cannot be sold."))
            record.state = "sold"

    def action_set_canceled(self):
        for record in self:
            if record.state == "sold":
                raise UserError(self.env._("Sold buildings cannot be canceled."))
            record.state = "canceled"

    @api.ondelete(at_uninstall=False)
    def _check_if_sold(self):
        for record in self:
            if record.state not in ("new", "canceled"):
                raise UserError(self.env._("This building cannot be deleted."))
        return self
