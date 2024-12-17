from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)
    partner_id = fields.Many2one(comodel_name='res.partner', required=True, string='Partner')
    property_id = fields.Many2one(comodel_name='estate.property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'Offer Price must be positive.')
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(fields.Date.to_date(record.create_date), days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = fields.Date.subtract(record.date_deadline - fields.Date.to_date(record.create_date)).days

    @api.model
    def create(self, vals):
        # vals returns the value in Integer but we need estate.property() object.
        property_id = self.env['estate.property'].browse(vals['property_id'])
        if property_id.offer_ids and any(offer.price >= vals['price'] for offer in property_id.offer_ids):
            raise ValidationError("You cannot create an offer lower than an existing offer.")
        property_id.state = 'received'

        return super(EstatePropertyOffer, self).create(vals)

    def action_offer_accepted(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'accepted'

            # set status 'refused' in the other offers of that particular property
            for offer in record.property_id.offer_ids:
                if offer.id != record.id:
                    offer.status = 'refused'
        return True

    def action_offer_refused(self):
        for record in self:
            record.status = 'refused'
        return True
