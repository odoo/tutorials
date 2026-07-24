from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    # Attributes
    _name = 'estate.property.offer'
    _description = "Real Estate Property Offer"
    _order = 'price desc'

    # Fields
    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        string="Status",
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)

    # Relational Fields
    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
        string="Property Type",
        store=True,
    )

    # Computed Fields
    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    # SQL Constraints
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        "The offer price must be strictly positive.",
    )

    # Compute / Inverse Methods
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date = record.create_date.date() if record.create_date else fields.Date.today()
            if record.date_deadline:
                record.validity = (record.date_deadline - date).days

    # CRUD Methods
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            record = self.env['estate.property'].browse(vals['property_id'])
            record._check_new_offer_price(vals['price'])
            record.state = 'offer_received'
        return super().create(vals_list)

    # Action Methods
    def action_accept(self):
        if self.filtered(lambda offer: offer.status in {'accepted', 'refused'}):
            raise UserError(self.env._("You can only accept pending offers."))
        for record in self:
            record.property_id._accept_offer(record.partner_id, record.price)
            other_offers = record.property_id.offer_ids - record
            other_offers.write({'status': 'refused'})
        self.write({'status': 'accepted'})
        return True

    def action_refuse(self):
        if self.filtered(lambda offer: offer.status == 'accepted'):
            raise UserError(self.env._("An accepted offer cannot be refused."))
        self.write({'status': 'refused'})
        return True
