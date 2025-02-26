from datetime import timedelta
from odoo import _, api, models,fields
from odoo import exceptions
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _inherit = ['mail.thread']
    _order = "id desc"

    name = fields.Char(required=True, tracking=True)
    description = fields.Text()
    postcode = fields.Char()
    image_1920 = fields.Image(store=True)
    date_availability = fields.Date(default= lambda self: fields.Datetime.today() + timedelta(days=90), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True , copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    total_area = fields.Float(string="Total Area (sqm)", compute="_compute_total_area", store=True)
    garden_orientation = fields.Selection(
        string="Type",
        selection=[
            ('north', 'North'),
            ('south','South'),
            ('east','East'),
            ('west','West')

        ],
    )
    status = fields.Selection(
        string="Status",
        selection=[
            ('new', 'New',),
            ('offer received','Offer Received'),
            ('offer accepted','Offer Accepted'),
            ('sold','Sold'),
            ('cancelled','Cancelled')
        ],
        default = 'new',
        required = True,
        copy = False,
    )
    active = fields.Boolean(default= True)
    property_type_id = fields.Many2one("estate.property.type",string="Property Type", ondelete="restrict")
    property_tag_id = fields.Many2many("estate.property.tag",string="Property Tag")
    buyer_id = fields.Many2one("res.partner",string="Buyer",copy=False)
    salesperson_id = fields.Many2one("res.users",string="Salesman",default=lambda self:self.env.user)
    offer_ids = fields.One2many("estate.property.offer","property_id")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price", store=True)
    user_id = fields.Many2one("res.users", string="Salesperson")
    company_id = fields.Many2one("res.company", required=True,default=lambda self: self.env.company, string="Agency")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            offer_prices = record.offer_ids.mapped('price')
            record.best_price = max(offer_prices) if offer_prices else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def action_set_sold(self):
        for record in self:
            if record.status == "cancelled":
                raise UserError(_("A cancelled property cannot be sold!"))

            accepted_offer = record.offer_ids.filtered(lambda o: o.status == 'accepted')
            if not accepted_offer:
                raise UserError(_("You need to accept an offer first!"))

            record.status = 'sold'
        return True

    def action_cancel(self):
        for record in self:
            if record.status == 'sold':
                raise UserError(_("A sold property cannot be cancelled."))
            record.status = 'cancelled'

    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive.'),
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if fields.float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_allowed_price = record.expected_price * 0.9
            if fields.float_compare(record.selling_price, min_allowed_price, precision_digits=2) == -1:
                raise ValidationError(
                    "Selling price cannot be lower than 90% of the expected price!"
                )

    @api.depends('offer_ids.status')
    def _compute_status_from_offer(self):
        for record in self:
            accepted_offer = record.offer_ids.filtered(lambda o: o.status == "accepted")
            if accepted_offer:
                record.status = "offer accepted"
            elif record.offer_ids:
                record.status = "offer received"
            else:
                record.status = "new"

    @api.ondelete(at_uninstall=False)
    def _prevent_deletion_if_not_new_or_cancelled(self):
        for record in self:
            if record.status not in ('new', 'cancelled'):
                raise exceptions.UserError(_("You can only delete properties in 'New' or 'Cancelled' state."))
