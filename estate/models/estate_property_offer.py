import logging
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    _check_price = models.Constraint(
        'CHECK (price > 0.00)',
        'The offer price must be greater than 0 and must be positive',
    )

    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline'
    )
    price = fields.Float(
        string='Price',
        required=True
    )

    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string='Status',
        copy=False
    )

    validity = fields.Integer(string="Validity (days)", default=7)

    # Many2one → res.partner (the buyer making the offer)
    partner_id = fields.Many2one(
        'res.partner',
        string='Buyer',
        required=True
    )

    # Many2one → estate.property (which property this offer is for)
    # This is the REQUIRED inverse field for the One2many on the property
    property_id = fields.Many2one(
        'estate.property',
        string='Property',
        required=True
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
        store=True
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            date = fields.Date.to_date(record.create_date) or fields.Date.today()
            record.date_deadline = fields.Date.add(date, days=record.validity)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_record = self.env['estate.property'].browse(vals.get('property_id'))
            existing_prices = property_record.offer_ids.mapped('price')
            if existing_prices and vals.get('price') <= max(existing_prices):
                raise ValidationError(_("Offer price must be higher than existing offers!"))
            property_record.state = 'offer_received'
        return super().create(vals_list)

    def _inverse_date_deadline(self):
        for record in self:
            date = (fields.Date.to_date(record.create_date)
                    or fields.Date.today())
            record.validity = (record.date_deadline - date).days

    def action_accept(self):
        self.ensure_one()
        if self.property_id.state in ('sold', 'cancelled'):
            raise ValidationError(_("Already sold or cancelled property can not accept the offer!"))
        (self.property_id.offer_ids - self).write({'status': 'refused'})
        self.write({'status': 'accepted'})
        self.property_id.write({
            'buyer_id': self.partner_id.id,
            'selling_price': self.price,
            'state': 'offer_accepted',
        })
        return True

    def action_refuse(self):
        if self.property_id.state == 'cancelled':
            raise UserError(_("You cannot reject an offer in a sold or cancelled property"))
        if self.status == 'accepted':
            self.property_id.selling_price = 0
            self.property_id.buyer_id = False
            self.property_id.state = 'offer_received'
        self.status = 'refused'
        return True

    @api.model
    def action_refused_cron(self):
        (self.search([('status', '!=', 'accepted'), ]).filtered(
            lambda o: o.create_date + timedelta(days=o.validity) < fields.Datetime.today()).write(
            {'status': 'refused'}))
