from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "estate property used to buy and sell houses"
    _order = "id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

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

    name = fields.Char()
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=lambda self: fields.Date.context_today(self) + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float()
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(
        default=2,
    )
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean(defaut=True)
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
    )

    state = fields.Selection(
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Recieved"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        string="Status",
        default='new',
        readonly=True,
        tracking=True,
        store=True,
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

    meeting_ids = fields.One2many(
        string='meeting',
        comodel_name='estate.property.meeting',
        inverse_name='property_id',
    )

    meeting_count = fields.Integer(
    compute="_compute_meeting_count",
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

    def offer_accepted(self):
        for rec in self:
            rec.state = 'offer_accepted'

  
    def offer_recieved(self):
        for rec in self:
            if any(rec.offer_ids and rec.offer_ids.status == 'new'):
                rec.state = 'offer_received'

    def sold(self):
        for rec in self:
            if rec.state == 'cancelled':
                message = "Property already cancelled"
                raise UserError(message)
            if rec.offer_ids and rec.state == 'offer_accepted':
                rec.state = 'sold'
            else:
                raise UserError(_("No accepted offer in prop"))

            message = "Wohoo!! Property Sold!!"

        return {
            "effect": {
                "fadeout": "fast",
                "message": message,
                "img_url": "/web/static/img/smile.svg",
                "type": "rainbow_man",
            },
        }

    def cancel(self):
        for rec in self:
            if rec.state == 'sold':
                message = "Cannot be cancelled as its already sold"
                raise UserError(message)
            if rec.state == 'cancelled':
                message = "Already cancelled cannot be cancelled again"
            rec.state = 'cancelled'

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
                'state': 'offer_accepted',
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

    @api.onchange('salesman_id')
    def _onchange_salesman(self):
        for rec in self:
            if rec.salesman_id:
                rec.progress_state = 'assigned'
            else:
                rec.progress_state = 'new'

    @api.ondelete(at_uninstall=False)
    def delete_new_sold(self):
        for rec in self:
            if rec.state not in ['new', 'cancelled']:
                raise UserError(_("Cannot delete this record it needs to be in either new or cancel to delete"))

    @api.depends('meeting_ids')
    def _compute_meeting_count(self):
        for rec in self:
            rec.meeting_count = len(rec.meeting_ids)
            
            
