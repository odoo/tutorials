from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "estate property"
    _order = 'id desc'

    # simple fields
    name = fields.Char()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available From", copy=False, default=fields.Datetime.add(fields.Datetime.now(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer("Living Area (sqm)", default=1)
    facades = fields.Integer(default=1)
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer("Garden Area (sqm)")
    active = fields.Boolean()

    garden_orientation = fields.Selection(
        selection=[('north', "North"), ('south', "South"), ('east', "East"), ('west', "West")],
        help="orientation of the garden relative to the property",
        )
    state = fields.Selection(
        string="Status",
        selection=[('new', "New"),
                   ('offer_received', "Offer Received"),
                   ('offer_accepted', "Offer Accepted"),
                   ('sold', "Sold"),
                   ('canceled', "Canceled"),
                   ],
        required=True,
        default='new',
        copy=False,
        )

    # relational fields
    property_type_id = fields.Many2one('estate.property.type', string="Type")
    buyer_id = fields.Many2one('res.partner', copy=False)
    salesperson_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    property_tag_ids = fields.Many2many('estate.property.tag', string="Tag")
    offer_ids = fields.One2many('estate.property.offer', "property_id")

    # computed fields
    total_area = fields.Integer(compute='_compute_area')
    best_price = fields.Float(compute='_compute_best_price')

    # sql constraints
    _sql_constraints = [
        ('check_positive_expected_price', 'CHECK(expected_price > 0)',
         'The expected price should be strictly positive number.'),
        ('check_positive_selling_price', 'CHECK(selling_price >= 0)',
         'The selling price should be a positive number.'),
    ]

    # python constraints
    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if ((not float_is_zero(record.selling_price, precision_digits=2))
                and (float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) < 0)):
                raise ValidationError("selling price can't be less than 90% of expected price")

    # compute methods
    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            self.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = None

    # action methods
    def action_set_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled propeties can't be sold")
            else:
                record.state = 'sold'
        return True

    def action_set_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("sold propeties can't be canceled")
            else:
                record.state = 'canceled'
        return True

    # overriding methods
    @api.ondelete(at_uninstall=False)
    def unlink_chcek_state(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError("Can only delete new or canceled properties!")
