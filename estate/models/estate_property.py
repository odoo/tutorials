from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class TestModel(models.Model):
    _name = "estate_property"
    _description = "Estate Property model"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)  #
    selling_price = fields.Float(readonly=True, copy=False)  #
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()  #
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')])
    active = fields.Boolean('Active', default=True)

    state = fields.Selection(
        string='Property Status',
        selection=[('New', 'New'), ('Offer Received', 'Offer Received'), ('Offer Accepted', 'Offer Accepted'), ('Sold', 'Sold'), ('Cancelled', 'Cancelled')],
        required=True,
        default="New")
    property_type_id = fields.Many2one("estate_property_type", string="Property Type")
    salesperson = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many("estate_property_tag", string="Property Tags")
    offer_ids = fields.One2many(comodel_name="estate_property_offer", inverse_name="property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_offer")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for property in self:
            if len(property.offer_ids) > 0:
                property.best_price = max(property.offer_ids.mapped('price'))
            else:
                property.best_price = 0.0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_orientation = "North"
            self.garden_area = 10
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def sell(self):
        for record in self:
            if not record.state == 'Offer Accepted':
                raise UserError("You cannot sell a property for which there is no accepted offer!")

            else:
                record.state = "Sold"
        return True

    def cancel(self):
        for record in self:
            if record.state == 'Sold':
                raise UserError("Sold properties cannot be cancelled!")

            else:
                record.state = "Cancelled"
        return True

    _sql_constraints = [
        ('strictly_positive_expected_price',
        'CHECK(expected_price > 0)',
         'The expected price should be strictly positive'),

         ('positive_seling_price',
        'CHECK(selling_price >= 0)',
         'The selling price should be positive'),

    ]

    @api.constrains('expected_price', 'selling_price')
    def filter_bad_offers(self):
        for property in self:
            if not float_is_zero(property.selling_price, precision_digits=6) and float_compare(property.selling_price, 0.9 * property.expected_price, precision_digits=6) < 0:
                raise ValidationError('The selling price is below the 90% threshold of the expected price')
        return True

    @api.ondelete(at_uninstall=False)
    def _unlink_if_offer_not_new_not_cancelled(self):
        if any(property.state not in ["New", "Cancelled"] for property in self):
            raise UserError("Can't delete an offer which is not cancelled or new!")
