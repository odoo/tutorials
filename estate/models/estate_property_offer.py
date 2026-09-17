from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
        store=True,
        string="Property Type"
    )
    
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ],
        string="Status", copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    
    property_id = fields.Many2one('estate.property', required=True, ondelete='cascade')

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'Offer price must be positive'),
    ]
    
    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    @api.depends("create_date", "validity")
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                start = record.create_date.date() if record.create_date else fields.Date.today()
                record.validity = (record.date_deadline - start).days

    @api.model
    def create(self, vals):
        property_id = self.env['estate.property'].browse(vals['property_id'])
        existing_max = max(property_id.offer_ids.mapped('price'), default=0)
        if vals.get('price', 0) < existing_max:
            raise UserError(
                f"The offer amount ({vals['price']:.2f}) cannot be lower than "
                f"an existing offer ({existing_max:.2f})."
            )
        property_id.state = 'offer_received'
        return super().create(vals)

    def action_accept(self):
        for record in self:
            accepted_others = record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted' and o != record)
            if accepted_others:
                raise UserError("Only one offer can be accepted per property.")
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'sold'
            return True

    def action_refuse(self):
            for record in self:
                record.status = 'refused'
            return True
