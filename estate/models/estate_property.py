from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = "id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Title', required=True, default='Unknown')
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postal Code')
    date_availability = fields.Date(
        string='Available From', copy=False, default=lambda self: fields.Date.today() + relativedelta(months=3)
    )
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(
        string='Selling Price', readonly=True, copy=False
    )
    living_area = fields.Integer(string='Living Area (sq m)')
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    facades = fields.Integer(string='Facades')
    has_garage = fields.Boolean(string="Has Garage ?")
    has_garden = fields.Boolean(string="Has Garden ?")
    garden_area = fields.Integer(string="Garden Area (sq m)")
    active = fields.Boolean(string="Is Active ?", default=True)
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
    )
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled")
        ],
        required=True, default="new", copy=False
    )
    property_type_id = fields.Many2one(
        "estate.property.type", ondelete='cascade', string="Property Type"
    )
    salesperson_id = fields.Many2one(
        "res.users", string="Sales Person", default=lambda self: self.env.user
    )
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    property_tags_ids = fields.Many2many(
        "estate.property.tag", string="Property Tags"
    )
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(
        string="Best Offer", compute="_compute_best_price", store=True
    )
    visit_ids = fields.One2many('estate.property.visit', 'property_id')
    issue_ids = fields.One2many('estate.property.issue', 'property_id')
    issue_count = fields.Integer(compute='_compute_issue_count')

    _check_expected_price = models.Constraint(
        'CHECK(expected_price > 0)', 'Price must be strictly positive'
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0

    @api.depends('visit_ids')
    def _compute_issue_count(self):
        data = dict(self.env['estate.property.issue']._read_group(
            [('property_id', 'in', self.ids)],
            groupby=['property_id'],
            aggregates=['__count']
        ))

        for record in self:
            record.issue_count = data.get(record, 0)
            # record.issue_count = len(record.issue_ids)

    @api.onchange('has_garden')
    def _onchange_garden(self):
        if self.has_garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_price = record.expected_price * 0.9
            if float_compare(
                record.selling_price,
                min_price,
                precision_digits=2
            ) < 0:
                raise ValidationError(_(
                    "The selling price cannot be lower than 90% of the expected price."
                ))

    def action_property_sold(self):
        if self.state == "cancelled":
            raise UserError(_("Cancelled property cannot be set as sold."))
        elif self.issue_ids.priority == '3' and self.issue_ids.state != "resolved":
            raise UserError(_("High priority issue is still not resolved"))
        else:
            self.state = "sold"
        return True

    def action_set_sold_rainbow_man(self):
        self.action_property_sold()

        return {
            'effect': {
                'fadeout': 'slow',
                'img_url': '/web/static/img/smile.svg',
                'type': 'rainbow_man',
            }
        }

    def action_property_cancelled(self):
        if self.state == "sold":
            raise UserError(_("Sold property cannot be set as cancelled"))
        else:
            self.state = "cancelled"
        return True

    def action_accept_best_offer(self):
        best_offer = self.offer_ids.filtered_domain(
            [('price', '=', self.best_price)])
        best_offer.action_offer_accepted()
        return True

    @api.ondelete(at_uninstall=False)
    def delete_state_check(self):
        for record in self:
            if record.state not in ('new', 'cancelled'):
                raise UserError(
                    _("Only New or Cancelled properties can be deleted"))
        return True
