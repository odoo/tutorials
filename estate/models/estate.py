from odoo import api, fields, models
from odoo.exceptions import ValidationError, UserError


class PartnerModel(models.Model):
    _inherit = 'res.partner'

    property_ids = fields.One2many('estate.property', 'buyer')

class UserModel(models.Model):
    _inherit = 'res.users'

    property_ids = fields.One2many('estate.property', 'seller')


class EstateModel(models.Model):
    _name = 'estate.property'
    _description = "Real Estate Properties"
    _order = 'id desc'
    _sql_constraints = [('check_expected_price', 'CHECK(expected_price > 0)', "The expected price must be positive."),
                        ('check_selling_price', 'CHECK(selling_price >= 0)', "The selling price must be positive."),
                        ]

    name = fields.Char(required=True)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    property_type_id = fields.Many2one('estate.property.type', string="Property Type")
    seller = fields.Many2one('res.users',
                             string="Salesman")
    buyer = fields.Many2one('res.partner',
                            string="Buyer")

    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Datetime(default=fields.Date.add(fields.Date.today(), months=3),
                                        copy=False)
    expected_price = fields.Float(required=True)
    best_price = fields.Integer(readonly=True, copy=False, compute='_compute_best_price')
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(string="Garden Orientation",
                                          selection=[('north', "North"),
                                                     ('east', "East"),
                                                     ('west', "West"),
                                                     ('south', "South"),
                                                     ])
    status = fields.Selection(selection=[('new', "New"),
                                         ('received', "Offer Received"),
                                         ('accepted', "Offer Accepted"),
                                         ('sold', "Sold"),
                                         ('canceled', "Canceled"),
                                         ],
                              default='new',
                              string="Status")
    total_area = fields.Integer(string="Total Area (sqm)", compute='_compute_total_area')
    active = fields.Boolean(default=True)

    @api.ondelete(at_uninstall=False)
    def _unlink_if_offered(self):
        for record in self:
            if record.status in ['new', 'canceled']:
                raise UserError("Cannot delete new or canceled property.")

    @api.depends('garden_area', 'living_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = ''

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.buyer and record.selling_price <= (0.9 * record.expected_price):
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

    def action_sell_property(self):
        for record in self:
            if record.status == 'canceled':
                raise UserError("Canceled properties cannot be sold.")
            else:
                record.status = 'sold'
            return True

    def action_cancel_property(self):
        for record in self:
            if record.status == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            else:
                record.status = 'canceled'
            return True
