from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property used to buy and sell houses"

    _positive_price = models.Constraint('CHECK (expected_price>=0)',
                    'Expected price must be positive',
                    )
    _selling_price = models.Constraint('CHECK(selling_price>=0)',
    'Selling price must be positive')

    request = fields.Text()
    estimated_cost = fields.Float(string="Estimated Cost")

    request_ids = fields.One2many(
        'estate.property.request',
        'request_id',
        string="Requests",
    )

    progress_state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('assigned', 'Assigned'),
            ('inprogress', 'In Progress'),
            ('done', 'done'),
        ],
        default='new',
    )

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(
        default=2,
    )
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(required=True)
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )

    state = fields.Selection(
        selection=[
            ("New", "New"),
            ("Offer Accepted", "offer_accepted"),
            ("Offer Received", "offer_received"),
            ("Sold", "Sold"),
            ("Cancelled", "Cancelled"),
        ],
    )
    status = fields.Selection(
        selection=[
            ('new', "New"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
            ('reset', "reset"),
        ],
        string="Status",
        default='new',
    )

    active = fields.Boolean(default=True)

    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
    )

    salesman_id = fields.Many2one(
        'res.users',
        string="Salesman",
        default=lambda self: self.env.user,
    )

    buyer_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        copy=False,
    )

    tag_ids = fields.Many2many(
        string="Tags",
        comodel_name='estate.property.tag',
    )

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers',
        )

    total_area = fields.Float(
        compute="_compute_total_area",
        string='Total Area',
        store=True,
        help="Auto Computed field",
        )
    best_price = fields.Integer(string="Best Price", compute="_compute_best_price")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_price = max(rec.offer_ids.mapped("price"))
            else:
                rec.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def sold(self):
        for rec in self:
            if rec.status == 'cancelled':
                message = "Property already cancelled"
                raise UserError(message)
            if rec.status == 'sold':
                message = "Already sold cannot be sold again"
            rec.status = 'sold'

    def cancel(self):
        for rec in self:
            if rec.status == 'sold':
                message = "Cannot be cancelled as its already sold"
                raise UserError(message)
            if rec.status == 'cancelled':
                message = "Already cancelled cannot be cancelled again"
            rec.status = 'cancelled'

    # def reset(self):
    #     properties = self.mapped('property_id')

    #     offers = self.env['estate.property.offer'].search([
    #         ('property_id', 'in', properties.ids)
    #     ])
    #     offers.write({'status': 'new'})

    #     properties.write({
    #         'selling_price': 0,
    #         'buyer_id': False,
    #         'state': 'new',
    #     })

    def accept_best_offer(self):
        for rec in self:
            offers = rec.offer_ids
            if not offers:
                raise UserError({"No offers to accept."})

            best_offer = offers.sorted('price', reverse=True)[0]

            offers.write({'status': 'offer_rejected'})
            best_offer.write({'status': 'offer_accepted'})

            rec.write({
                'selling_price': best_offer.price,
                'status': 'sold',
            })

    @api.constrains('selling_price')
    def _selling_price(self):
        for rec in self:
            if float_is_zero(rec.selling_price, precision_digits=2):
                continue
            min_price = rec.expected_price * 0.9
            if float_compare(rec.selling_price, min_price, precision_digits=2) < 0:
                message = "Price cannot be less than 90%"
                raise ValidationError(message)

    def action_assign(self):
        for rec in self:
            rec.progress_state = 'assigned'

    def action_done(self):
        for rec in self:
            if rec.progress_state != 'inprogress':
                raise UserError(_("Work must be In Progress before marking Done."))
            rec.progress_state = 'done'

    def action_start(self):
        for rec in self:
            rec.progress_state = 'inprogress'

    def action_stop(self):
        for rec in self:
            rec.progress_state = 'done'

    @api.onchange('technician')
    def _onchange_technician(self):
        for rec in self:
            if rec.technician():
                rec.progress_state = 'assigned'
            else:
                rec.progress_state = 'new'
