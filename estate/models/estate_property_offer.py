import logging
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class EstatePropertyOffer(models.Model):
    # Private attributes
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "price desc"

    # Fields — all grouped together
    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[('Accepted', "Accepted"), ('Refused', "Refused")],
        string="Status", copy=False,
    )
    property_type_id = fields.Many2one(
        "estate.property.type", string="Property Type Id", store=True,
        related="property_id.property_type_id")
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity date", default=7)
    is_spam = fields.Boolean(string="spam", default=False, copy=False)
    date_deadline = fields.Date(
        string="Deadline date", compute="_compute_date_deadline",
        inverse="_inverse_date_deadline", store=True)
    expired_offers = fields.Integer(string="expired offers", compute="_compute_expired_offers")

    # Compute, inverse, search methods — in the same order as field declaration
    @api.depends('property_id.offer_ids.status', 'property_id.offer_ids.date_deadline')
    def _compute_expired_offers(self):
        for record in self:
            record.expired_offers = len(record.property_id.offer_ids.filtered(
                lambda o: o.date_deadline and o.date_deadline < fields.Date.today()
                and o.status not in ('Accepted', 'Refused'),
            ))

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            base = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base + timedelta(record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - base).days

    def _compute_display_name(self):
        for record in self:
            record.display_name = record.property_id.name

    # Constrains methods
    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price < 0:
                raise ValidationError(_("price cannot be less than 0"))

    # CRUD methods
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('property_id') and vals.get('price'):
                property = self.env['estate.property'].browse(vals['property_id'])
                if vals.get('price') < max(property.offer_ids.mapped('price'), default=0):
                    raise UserError(_("an offer lower than the max offer's price cannot be accepted"))
                if property.state == 'new':
                    property.state = 'offer_received'
        return super().create(vals_list)

    # Action methods
    def action_accept(self):
        self.ensure_one()
        if 'Accepted' in self.property_id.offer_ids.mapped('status'):
            raise UserError(_("An offer has already been accepted for this property"))
        self.status = 'Accepted'
        self.property_id.write({
            'state': 'offer_accepted',
            'buyer_id': self.partner_id,
            'selling_price': self.price,
        })
        self.property_id.offer_ids.filtered(lambda o: not o.status).write({'status': 'Refused'})

    def action_refuse(self):
        self.ensure_one()
        self.status = 'Refused'

    def action_create_booking(self):
        self.ensure_one()
        booking = self.env['estate.property.booking'].search([
            ('property_id', '=', self.property_id.id),
        ], limit=1)
        if not booking:
            booking = self.env['estate.property.booking'].create({
                'property_id': self.property_id.id,
                'customer_id': self.partner_id.id,
                'offer_id': self.id,
            })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property.booking',
            'view_mode': 'form',
            'res_id': booking.id,
            'target': 'new',
        }

    # Business methods
    def _auto_ref_expired_offers(self):
        expired_offers = self.search([
            ('date_deadline', '<', fields.Date.today()),
            ('status', 'not in', ['Accepted', 'Refused']),
        ])
        _logger.info("Auto-refusing %d expired offers", len(expired_offers))
        expired_offers.write({'status': 'Refused'})
