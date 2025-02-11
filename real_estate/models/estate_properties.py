from odoo import fields, api, models  # type: ignore
from odoo.exceptions import UserError, ValidationError  # type: ignore
from odoo.tools.float_utils import float_compare, float_is_zero  # type: ignore


class EstateProperties(models.Model):
    _name = "estate.properties"
    _description = 'Estate Properties'
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False,  default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Orientation', selection=[(
        'north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], default="east")
    state = fields.Selection(string='State', selection=[('new', 'New'), ('offer_recieved', 'Offer Received'), (
        'offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], default="new", copy=False, required=True)
    property_type_id = fields.Many2one(
        comodel_name='estate.properties.type', string='Type')
    partner_id = fields.Many2one(
        'res.partner', string='Buyer', index=True,  copy=False)
    users_id = fields.Many2one(
        'res.users', string='Salesperson', index=True,  default=lambda self: self.env.user)
    tags_id = fields.Many2many('estate.properties.tags', string="Tags")
    offer_ids = fields.One2many(
        'estate.properties.offer', 'property_id', string="Offer")
    total_area = fields.Float(compute='_compute_total_area', store=True)
    best_offer = fields.Float(compute='_compute_best_price')

# Constraints added to table fields using sql
    _sql_constraints = [
        ('expected_price', 'CHECK(expected_price > 0)',
         'Expected Price should be greater than 0'),
        ('selling_price', 'CHECK(selling_price >= 0)',
         'Selling Price should be greater than 0'),
    ]

    @api.depends('garden_area', 'living_area')
# this function is used for compute.compute is a read only function. If you want to save data make store=True in field
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0.00

    @api.onchange("garden")
    def _trace_action(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = ""

    def action_property_sold(self):
        if self.state == "cancelled":
            raise UserError("Cancelled property cannot be sold")
        self.state = "sold"

    def action_property_rejected(self):
        if self.state == "sold":
            raise UserError("Sold property cannot be cancelled")
        self.state = "cancelled"


# Constraints added to table fields using python

    @api.constrains('selling_price', 'expected_price')
    def check_price(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price,
                                  precision_rounding=0.01)
                and
                float_compare(
                    record.selling_price, record.expected_price * .9, precision_rounding=0.01) < 0
            ):
                raise ValidationError(
                    "The selling price cannot be lower than 90% of the expected price.")

    @api.ondelete(at_uninstall=False)
    def _prevent_accept_records(self):
        for record in self:
            if record.state not in ['new','cancelled']:
                raise ValidationError('Cannot delete this property')