import logging

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

_logger = logging.getLogger(__name__)


class EstateProperty(models.Model):
    _name = 'estate.property'
    _inherit = ['mail.thread']
    _description = "Real Estate Property"
    _order = 'id desc'
    _check_expected_price = models.Constraint(
        definition='CHECK (expected_price > 0)',
        message='The selling price must be positive do not enter negative values',
    )
    _check_selling_price = models.Constraint(
        definition='CHECK (selling_price > 0)',
        message='The selling price must be positive do not enter negative values',
    )
    active = fields.Boolean(default=True)
    bedrooms = fields.Integer(default=2)
    best_price = fields.Float(string="Best Offer", compute='_compute_best_price', store=True)
    date_availability = fields.Date(
        string="Available From",
        default=lambda self: fields.Date.add(fields.Date.context_today(self), months=3),
        copy=False
    )
    description = fields.Text()
    expected_price = fields.Float(required=True)
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West")
        ],
        help="Direction the garden faces"
    )
    living_area = fields.Integer(string="Living Area (sqm)")
    name = fields.Char(string="Title", required=True)
    postcode = fields.Char()
    sequence = fields.Integer()
    selling_price = fields.Float(readonly=True, copy=False)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        required=True,
        default='new',
        copy=False
    )
    total_area = fields.Integer(compute='_compute_total_area', store=True)

    # Many2one: property type (House, Apartment, etc.)
    property_type_id = fields.Many2one(
        'estate.property.type',
        string='Property Type'
    )

    # Many2one: buyer (from res.partner — contacts)
    buyer_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        copy=False
    )

    # Many2one: salesperson (from res.users — Odoo users)
    salesperson_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        default=lambda self: self.env.user
    )

    offer_ids = fields.One2many(
        'estate.property.offer',
        'property_id',
        string='Offers'
    )

    tag_ids = fields.Many2many(
        'estate.property.tag',
        string='Tags'
    )

    visit_ids = fields.One2many(
        'estate.visit',
        'property_id',
        string='Visits'
    )

    visits_count = fields.Integer(string="Number of Visits", compute='_compute_visits_count')

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            min_price = record.expected_price * 0.90
            if float_compare(record.selling_price, min_price, precision_digits=2) < 0:
                raise ValidationError(
                    f"Selling price ({record.selling_price:.2f}) cannot be "
                    f"lower than 90% of expected price ({min_price:.2f})."
                )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for rec in self:
            rec.best_price = max(rec.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    @api.ondelete(at_uninstall=False)
    def _unlink_ondelete(self):
        for record in self:
            if record.state not in ['new', 'cancelled']:
                raise ValidationError("Can't delete Property!")

    def action_sold(self):
        _logger.info("--send mail is starting--")
        self.ensure_one()
        template = self.env.ref('estate.send_email_templates', raise_if_not_found=False)
        ctx = {
            'default_model': 'estate.property',
            'default_res_ids': self.ids,
            'default_template_id': template.id,
            'force_email': True,
            'default_partner_ids': [self.buyer_id.id, self.salesperson_id.partner_id.id],
            'sales_person': self.salesperson_id.name,
            'property_name': self.name,
            'buyer_name': self.buyer_id.name,
            'selling_price': self.selling_price

        }

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
        _logger.info("--sending mail is end--")
        if self.state == 'cancelled':
            raise ValidationError("Cancelled properties cannot be sold.")
        self.state = 'sold'
        _logger.info("--action sold is ended--")

        return action

    def best_offer(self):
        for record in self:
            record.offer_ids.filtered(lambda o: o.price == record.best_price)[:1].action_accept()

    def action_rest(self):
        self.ensure_one()
        self.write({
            'state': 'new',
            'selling_price': 0.0,
            'buyer_id': '',
        })
        self.mapped('offer_ids').write({'status': False})
        return True

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise ValidationError("Sold properties cannot be cancelled.")
            record.state = 'cancelled'
        return True

    @api.depends('visit_ids')
    def _compute_visits_count(self):
        for rec in self:
            rec.visits_count = len(rec.visit_ids)

    def action_see_visits(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('estate.estate_visit_action')
        action['domain'] = [('property_id', '=', self.id)]
        return action

    def action_send_mail_property(self):
        _logger.info("--send mail is starting--")
        self.ensure_one()
        template = self.env.ref('estate.send_email_templates', raise_if_not_found=False)

        ctx = {
            'default_model': 'estate.property',
            'default_res_ids': self.ids,
            'default_template_id': template.id,
            'force_email': True,
            'default_partner_ids': [self.buyer_id.id, self.salesperson_id.partner_id.id],
            'sales_person': self.salesperson_id.name,
            'property_name': self.name,
            'buyer_name': self.buyer_id.name,
            'selling_price': self.selling_price

        }

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
        _logger.info("--sending mail is stopped--")
        return action
