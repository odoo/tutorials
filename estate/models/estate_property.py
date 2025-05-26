from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Properties'
    _order = 'id desc'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available from", copy=False, default=lambda: fields.Date.add(value=fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', "New"), ('offer_received', "Offer Received"), ('offer_accepted', "Offer Accepted"), ('sold', "Sold"), ('cancelled', "Cancelled")
        ], required=True, default='new'
    )

    type_id = fields.Many2one('estate.property.type', string="Property Type")
    buyer_id = fields.Many2one('res.partner', string="Buyer")
    salesperson_id = fields.Many2one('res.users', string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for estate_property in self:
            area = estate_property.living_area
            if estate_property.garden:
                area += estate_property.garden_area
            estate_property.total_area = area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for estate_property in self:
            if estate_property.offer_ids:
                estate_property.best_price = max(estate_property.offer_ids.mapped('price'))
            else:
                estate_property.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def sold_property(self):
        for estate_property in self:
            if estate_property.state == 'cancelled':
                raise UserError("You can't sold a cancelled property !")
            estate_property.state = 'sold'

        return True

    def cancel_property(self):
        for estate_property in self:
            if estate_property.state == 'sold':
                raise UserError("You can't cancel a sold property !")
            estate_property.state = 'cancelled'

        return True

    _sql_constraints = [
        ('check_expected_price_positive', 'CHECK(expected_price > 0)',
        "The expected price must be strictly positive"),
        ('check_selling_price_positive', 'CHECK(selling_price >= 0)',
        "The selling price must be positive")
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_percentage(self):
        for estate_property in self:
            if not estate_property.offer_ids.filtered(lambda x: x.status == 'accepted'):
                return True

            if float_compare(estate_property.selling_price, estate_property.expected_price * 0.9, precision_digits=2) == -1:
                raise ValidationError(self.env._("The selling price cannot be lower than 90% of the expected price"))

    @api.ondelete(at_uninstall=False)
    def _unlink_property(self):
        for estate_property_id in self.ids:
            estate_property = self.env['estate.property'].browse(estate_property_id)
            if not estate_property.state in ('new', 'cancelled'):
                raise UserError(self.env._("You can only delete property in a New or Cancelled state"))
