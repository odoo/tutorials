from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, exceptions, tools


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "A new model to store real estate properties"
    _check_expected = models.Constraint('CHECK(expected_price > 0)', 'The price must be positive!')
    _check_selling = models.Constraint('CHECK(selling_price >= 0)', 'The price must be positive!')
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: date.today() + relativedelta(months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ],
        default='new',
        required=True,
        copy=False,
    )
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", required=True)
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tags_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Integer(compute="_compute_total_area", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price", string="Best Offer")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_offer_ids(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.constrains('selling_price')
    def _check_selling_above_90(self):
        for record in self:
            for offer in record.offer_ids:
                if offer.status == 'accepted':
                    offer_accepted = True
            compare = tools.float_utils.float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2)
            if offer_accepted and compare != 1:
                raise exceptions.ValidationError("Cannot sell bellow 90% of expected price!")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise exceptions.UserError('Cannot delete a property with offers or that is sold!')
            elif len(record.offer_ids) > 0:
                raise exceptions.UserError('Cannot delete a property that already recieved offers!')
        return True

    def property_set_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise exceptions.UserError('Canceled propery cannot be sold!')
            elif record.state != 'offer_accepted':
                raise exceptions.UserError('An offer must be accepted in order to mark a property as sold!')
            else:
                record.state = 'sold'
        return True

    def property_set_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError('Sold property cannot be cancelled!')
            else:
                record.state = 'canceled'
        return True
