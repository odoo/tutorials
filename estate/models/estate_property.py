from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char()
    date_availability = fields.Date(
        string="Available From",
        copy=False,
        default=lambda self: fields.Date.add(fields.Date.today(), days=90)
    )
    expected_price = fields.Float()
    best_price = fields.Float(compute='_compute_best_price', readonly=True, store=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(string="Bedrooms", default=0)
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Has garage")
    living_area = fields.Float(string="Living_Area(sqm)")
    garden = fields.Boolean(string="Has garden")
    garden_area = fields.Float(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
        string="Garden Orientation",
    )
    total_area = fields.Float(compute='_compute_total_area', readonly=True, store=True)
    last_seen = fields.Datetime(string='Last Seen', default=fields.Datetime.now)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        string="Status",
        default='new'
    )

    salesman_id = fields.Many2one(comodel_name='res.users', string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one(comodel_name='res.partner', string="Buyer", copy=False)
    property_type_id = fields.Many2one(comodel_name='estate.property.type', string="Property Type")
    tag_ids = fields.Many2many(comodel_name='estate.property.tag', string="Tags")
    offer_ids = fields.One2many(comodel_name='estate.property.offer', inverse_name='property_id')

    _check_expected_prices = models.Constraint(
        'CHECK(expected_price > 0)', "The expected price must be strictly positive.")
    _check_selling_price = models.Constraint(
        'CHECK(selling_price > 0)', "The selling price must be strictly positive.")

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue

            limit_price = record.expected_price * 0.9

            if float_compare(record.selling_price, limit_price, precision_digits=2) == -1:
                raise ValidationError(
                    self.env._("The selling price cannot be lower than 90% of the expected price! Check your offers or adjust the expected price.")
                )

    @api.constrains('offer_ids')
    def _check_creating_offer(self):
        properties = self.filtered(lambda r: r.state in ('sold', 'cancelled', 'offer_accepted'))

        if properties:
            raise ValidationError(
                self.env._("The property is already Sold, Cancelled, or Offer Accepted! You cannot make a new offer.")
            )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0

    @api.onchange('offer_ids')
    def _onchange_offer_ids(self):
        for record in self:
            if record.state != 'sold':
                if record.offer_ids:
                    if 'accepted' not in record.offer_ids.mapped('status'):
                        record.state = 'offer_received'
                else:
                    record.state = 'new'

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise UserError("You can only delete a property if its state is 'New' or 'Cancelled'.")

    def action_sell(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("A canceled property cannot be sold!")
            elif record.state == 'sold':
                raise UserError("The property is already sold!")

            record.state = 'sold'

            for offer in record.offer_ids:
                if offer.status != 'accepted':
                    offer.status = 'refused'

        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("A Sold property cannot be canceled!")
            record.state = 'cancelled'

        return True
