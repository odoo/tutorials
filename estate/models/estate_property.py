from odoo import api, exceptions, fields, models
from datetime import date, timedelta

class Property(models.Model):
    _name = "estate.property"
    _description = "Test description for estate.property model"

    name               = fields.Char(required=True)
    expected_price     = fields.Float(required=True)

    _check_expected_price = models.Constraint(
        "CHECK(expected_price > 0)",
        "The expected price must be strictly positive"
    )

    property_type_id   = fields.Many2one("estate.property.type", string="Property Type")
    state              = fields.Selection(
        string='State',
        selection=[("new", "New"), ("offerreceived", "Offer Received"), ("offeraccepted", "Offer accepted"), ("sold", "Sold"), ("cancelled", "Cancelled")],
        default="new"
    )
    description        = fields.Text()
    postcode           = fields.Char()
    selling_price      = fields.Float(copy=False, readonly=True)

    _check_selling_price = models.Constraint(
        "CHECK (selling_price >= 0)",
        "The selling price must be positive"
    )

    date_availability  = fields.Date(copy=False, default=date.today() + timedelta(days=90))
    bedrooms           = fields.Integer(default=2)
    living_area        = fields.Integer()
    facades            = fields.Integer()
    garage             = fields.Boolean()
    garden             = fields.Boolean()

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    garden_area        = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[("north","North"), ("south", "South"), ("east","East"), ("west", "West")])

    active             = fields.Boolean(default=True)
    buyer_id           = fields.Many2one("res.partner", string="Buyer")
    salesperson_id     = fields.Many2one("res.users", string="Salesperson", copy=False, default=lambda self: self.env.user)

    tags_ids           = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids          = fields.One2many("estate.property.offer", "property_id", string="Offers")

    total_area         = fields.Float(compute="_compute_total_area")

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    best_price         = fields.Float(compute="_compute_best_price")

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max([o.price for o in record.offer_ids]) if len(record.offer_ids) > 0 else 0

    def action_property_cancel(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("A sold property cannot be cancelled.")
            else:
                record.state = "cancelled"
        return True

    def action_property_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise exceptions.UserError("A cancelled property cannot be sold.")
            else:
                record.state = "sold"
        return True