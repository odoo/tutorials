from random import randint

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero, float_compare, _


class RealEstate(models.Model):
    _name = 'real.estate'
    _description = 'Real Estate Property'
    _order = "id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(required=True, tracking=True)
    property_type_id = fields.Many2one(
        "real.estate.property.type", string="Property Type")
    color = fields.Integer(default=_get_default_color)
    street_address = fields.Char()
    description = fields.Text()
    postcode = fields.Integer()
    date_availability = fields.Datetime(default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    # default=date.today() + timedelta(days=90)
    expected_price = fields.Float()
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    bathrooms = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ])
    active = fields.Boolean(default=True)
    tag_ids = fields.Many2many(
        "real.estate.tag", string="Tags", ondelete='cascade')
    offer_ids = fields.One2many(
        "real.estate.property.offer", "property_id", string="Offers", tracking=True)
    total_area = fields.Float(compute="_compute_total", store=True)
    best_price = fields.Float(
        string="Best Offer",
        compute="_compute_best_price",
        search="_search_best_price", tracking=True)
    # ist_time = fields.Char(
    #     string="Created On (IST)",
    #     compute="_compute_create_date_ist",
    #     store=True)
    stage = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled'),
    ], default='new', tracking=True)
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False, tracking=True)
    selling_price = fields.Float()
    maintenance_request_ids = fields.One2many(
        "real.estate.property.maintenance.request", "property_id", string="Maintenance Requests")
    total_maintenance_cost = fields.Float(compute="_compute_total_maintenance_cost", store=True, string="Total Cost")
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user
    )
    _check_expected_price_positive = models.Constraint(
        'CHECK(expected_price > 0)',
        'The expected price must be strictly positive.',
    )

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for rec in self:
            if float_is_zero(rec.selling_price, precision_rounding=0.01):
                continue
            if float_compare(
                    rec.selling_price,
                    rec.expected_price * 0.9,
                    precision_rounding=0.01) < 0:
                raise ValidationError(_(
                    'The selling price cannot be lower than 90% of the expected price.'))

    # @api.depends("offer_ids.price")
    # def _compute_best_price(self):
    #     for record in self:
    #         record.best_price = max(record.offer_ids.mapped("price"), default=0.0)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        dataa = dict(self.env['real.estate.property.offer']._read_group(
            domain=[('property_id', 'in', self.ids)],
            groupby=['property_id'],
            aggregates=['price:max'],
        ))
        for record in self:
            record.best_price = dataa.get(record, 0.0)

    def _search_best_price(self, operator, value):
        records = self.search([])
        domain = [('best_price', operator, value)]
        filtered = records.filtered_domain(domain)
        return [('id', 'in', filtered.ids)]

    # def _search_best_price(self, operator, value):
    #     if operator not in ('=', '!=', '<', '<=', '>', '>='):
    #         return NotImplemented
    #     groups = self.env['real.estate.property.offer']._read_group(
    #         [],
    #         ['property_id'],
    #         having=[(f'price:max', operator, value)]
    #     )
    #     property_ids = [g[0].id for g in groups if g and g[0]]
    #     return [('id', 'in', property_ids)]

    @api.depends('maintenance_request_ids.cost')
    def _compute_total_maintenance_cost(self):
        for record in self:
            costs = record.maintenance_request_ids.mapped('cost')
            record.total_maintenance_cost = sum(costs) if costs else 0.0

    @api.depends('living_area', 'garden_area')
    def _compute_total(self):
        for rec in self:
            rec.total_area = (rec.living_area or 0) + (rec.garden_area or 0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _check_property_delete(self):
        invalid = self.filtered_domain([('stage', 'not in', ('new', 'cancelled'))])
        if invalid:
            raise UserError(
                "You can only delete properties in New or Cancelled state."
            )

    # @api.depends('create_date')
    # def _compute_create_date_ist(self):
    #     for rec in self:
    #         if rec.create_date:
    #             ist_dt = fields.Datetime.context_timestamp(
    #                 rec, rec.create_date
    #             )
    #             rec.ist_time = ist_dt.strftime("%Y-%m-%d %H:%M:%S")
    #         else:
    #             rec.ist_time = False

    def action_cancel(self):
        if self.stage == 'sold':
            raise UserError("A sold property cannot be cancelled.")
        self.stage = 'cancelled'

    def action_sold(self):
        if self.stage == 'cancelled':
            raise UserError("A cancelled property cannot be sold.")
        maintenance_request = self.maintenance_request_ids.filtered_domain([('status', '!=', 'done')])
        if maintenance_request:
            raise UserError("Property cannot be sold , there is any maintenance request not done")
        if not self.selling_price or not self.buyer_id:
            raise UserError("Cannot sell without a selling price and buyer.")

        ctx = {
            'default_model': 'real.estate',
            'default_res_ids': self.ids,
            'default_partner_ids': [
                self.buyer_id.id,
                self.salesperson_id.partner_id.id
            ],
        }
        mail_template = self.env.ref('real_estate.mail_template_data_real_estate')
        if mail_template:
            ctx.update({
                'default_template_id': mail_template.id,

            })
        action = {
            'name': _('Send'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }
        self.stage = 'sold'
        return action

    def action_best_offer(self):
        for record in self.offer_ids:
            if record.price == self.best_price:
                record.action_accept()

    def action_print_sale_doc(self):
        return self.env.ref('real_estate.real_estate_report_action_property_sale').report_action(self)
