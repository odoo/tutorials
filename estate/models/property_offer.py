from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    # Model Attributes
    _name = 'estate.property.offer'
    _description = 'Property Offer Model'
    _order = 'price desc'

    # SQL Constraints
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0.00)', "The offer price must be strictly positive")
    ]

    # Basic Fields
    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        string="Status",
        copy=False,
        selection = [
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ]
    )
    validity = fields.Integer(string="Validity", default=7)

    # Relational Fields
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    # Computed Fields
    date_deadline = fields.Date(string="Date Deadline", compute='_compute_validity', inverse='_inverse_validity')

    # Computed Methods
    @api.depends('create_date', 'validity')
    def _compute_validity(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_validity(self):
        for record in self:
            if record.date_deadline:
                create_date = record.create_date.date() if record.create_date else fields.Date.today()
                record.validity = (record.date_deadline - create_date).days

    # CRUD
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            property = self.env['estate.property'].browse(property_id)
            if property.state == 'offer_accepted':
                raise UserError(_("You cannot place an offer on a offer accepted property."))
            elif property.state == 'sold':
                raise UserError(_("You cannot place an offer on a sold property."))
            elif property.best_price >= vals.get('price'):
                raise UserError(_(f"A higher or equal offer already exists, increase your offer price.\n(It should be more than {property.best_price})"))
            property.state = 'offer_received'
        return super(PropertyOffer, self).create(vals_list)

    # Actions
    def action_accepted(self):
        self.ensure_one()
        if self.property_id.state == 'sold':
            raise UserError(_("Property already sold"))
        elif self.property_id.state == 'cancelled':
            raise UserError(_("Cancelled property's offer can not be accepted"))
        elif self.status == 'accepted':
            raise UserError(_("Buyer of property is already accepted"))
        for offer in self.property_id.offer_ids:
            if offer.id != self.id:
                offer.status = 'refused'
            else:
                self.write({'status': 'accepted'})
                self.property_id.write({
                    'state': 'offer_accepted',
                    'selling_price': self.price,
                    'buyer_id': self.partner_id
                })

    def action_refused(self):
        self.ensure_one()
        if self.property_id.state == 'sold':
            raise UserError(_("Property already sold"))
        elif self.property_id.state == 'cancelled':
            raise UserError(_("Cancelled property's offer can not be accepted"))
        elif self.status == 'refused':
            raise UserError(_("Buyer of property is already refused"))
        self.status = 'refused'
