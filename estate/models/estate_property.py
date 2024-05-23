from dateutil.utils import today

from odoo.tools.date_utils import add

from odoo import fields, models, api


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate base property model"

    # Reserved fields
    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[("new", "New"), ("offer_received", "Offer Received"), ("offer_accepted", "Offer Accepted"),
                   ("sold", "Sold"), ("canceled", "Canceled")],
        default="new",
        required=True,
        copy=False
    )

    # Model fields
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=add(today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")]
    )

    # Relational fields
    buyer = fields.Many2one("res.partner", copy=False)
    salesman = fields.Many2one("res.users", default=lambda self: self.env.user)
    property_type_id = fields.Many2one("estate.property.type")
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    # Computed fields
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_offer")

    # Computation methods
    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    # Onchange listeners
    @api.onchange("garden")
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_orientation = "north"
                record.garden_area = 10
            else:
                record.garden_orientation = None
                record.garden_area = None

    # Buttons methods
    def action_set_canceled(self):
        for record in self:
            record.state = "canceled"

    def action_set_sold(self):
        for record in self:
            record.state = "sold"

    def action_refuse_all_offer(self):
        for record in self:
            for offer in record.offer_ids:
                offer.status = "refused"
