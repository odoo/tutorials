from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _default_date_availability(self):
        return fields.Date.today() + relativedelta(months=3)

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    property_type = fields.Many2one("estate.property.type")
    sales_person = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", copy=False)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="offers")
    date_availability = fields.Date(
        copy=False,
        default=_default_date_availability,
        # default=lambda self: fields.Date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(required=True, tracking=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(
        compute="_compute_garden_details",
        store=True,
        readonly=False,
    )
    garden_orientation = fields.Selection(
        [('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
        compute="_compute_garden_details",
        store=True,
        readonly=False,
    )
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_recieved', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    active = fields.Boolean(default=True)
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(
        compute="_compute_best_price", search="_search_best_price"
    )

    sq_area = fields.Float(compute="_compute_computed_area")
    maintenance_ids = fields.One2many(
        'estate.property.maintenance', 'property_id', string="Maintenance"
    )

    @api.onchange("state")
    def _onchange_state_validation(self):
        if self.state == 'sold' and self._origin.state == 'cancelled':
            self.state = 'cancelled'
            raise ValidationError(message="cancelled properties cannot be sold")

    def _search_best_price(self, operator, value):
        groups = self.env["estate.property.offer"]._read_group(
            domain=[],
            groupby=["property_id"],
            aggregates=["price:max"],
            having=[("price:max", operator, value)],
        )
        property_ids = [res_group[0].id for res_group in groups if res_group[0]]
        return [("id", "in", property_ids)]

    @api.depends("total_area")
    def _compute_computed_area(self):
        for property in self:
            property.sq_area = property.total_area**2

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for property in self:
            # prices = [offer.price for offer in property.offer_ids]
            prices = property.offer_ids.mapped("price")
            property.best_price = max(prices) if prices else 0.0

    # unsafe for business logic and  only works in form view and list
    # (if editable) (triggered on user interaction)
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area, self.garden_orientation = 10, 'north'
        else:
            self.garden_area, self.garden_orientation = 0, False

    # safe for business logic
    @api.depends("garden")
    def _compute_garden_details(self):
        for property in self:
            if property.garden:
                property.garden_area, property.garden_orientation = 10, 'north'
            else:
                property.garden_area, property.garden_orientation = 0, False

    def action_set_state_cancel(self):
        for record in self:
            record.state = "cancelled"
        return True

    def action_set_state_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError(message='cancelled properties cannot be sold')
            record.state = "sold"
        return True
