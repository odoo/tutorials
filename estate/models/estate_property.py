from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "manage properties"
    _order = "id desc"

    name = fields.Char(required=True, default="Unknown")
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(string="Availability", copy=False, default=lambda x: fields.Datetime.add(fields.Datetime.today(), months=3))
    expected_price = fields.Float(string="Excepted price", required=True)
    selling_price = fields.Float(string="Selling price", readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living area")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden area")
    garden_orentation = fields.Selection(
        string="Garden orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('west', 'West'),
            ('east', 'East')
            ])

    active = fields.Boolean(default=True)
    state = fields.Selection(default='new', selection=[('new', 'New'),
                                                       ('offer_received', 'Offre Received'),
                                                       ('offer_accepted', 'Offer Accepted'),
                                                       ('sold', 'Sold'),
                                                       ('canceled', 'Canceled'),
                                                       ])

    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.company, required=True)
    tags_ids = fields.Many2many("estate_property_tags", string="Tags")
    salesman_id = fields.Many2one("res.users", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    estate_property_type = fields.Many2one("estate_property_type", string="Property Type")
    offer_ids = fields.One2many(comodel_name="estate_property_offer", inverse_name="property_id", string="Offers")

    total_area = fields.Integer(compute="_compute_area", string="Total area")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    _sql_constraints = [
        ('check_price_positive', 'CHECK(expected_price >= 0)', 'The price should be higher than 0'),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)', 'The selling price should be higher than 0'),
        ('check_unique_name', 'UNIQUE(name)', 'The name of the property should be unique'),
    ]

    @api.ondelete(at_uninstall=False)
    def _unlink_if_state_match(self):
        for property in self:
            if property.state not in ['new', 'canceled']:
                raise UserError(_("You can't delete active properties"))

    @api.depends("garden_area", "living_area")
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange("garden")
    def _update_garden_values(self):
        if self.garden:
            self.garden_area = 20
            self.garden_orentation = 'north'
        else:
            self.garden_area = 0
            self.garden_orentation = False

    def mark_as_sold(self):
        if 'canceled' in self.mapped("state"):
            raise UserError(_("You can't set a canceled property to sold"))
        self.state = "sold"

    def mark_as_canceled(self):
        for record in self:
            if record.state == "sold":
                raise UserError(_("You can't cancel a sold property"))
            else:
                record.state = "canceled"

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.expected_price, 2) and not float_is_zero(record.selling_price, 2):
                if float_compare(record.selling_price, (record.expected_price * 0.9), 2) == -1:
                    raise ValidationError(_("Selling price shoudn't be lower than 90% of expected price"))
