from datetime import timedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'
    _order = 'price desc'

    price = fields.Float(string='Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status', copy=False, readonly=True)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(compute='_compute_total_days', inverse='_inverse_total_days', string='Deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0.0)', 'The offer price must be strictly positive.')
    ]

    @api.depends('create_date', 'validity')
    def _compute_total_days(self):
        for record in self:
            record.date_deadline = fields.Date.add((record.create_date or fields.date.today()), days=record.validity)

    def _inverse_total_days(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days if record.date_deadline else 0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_rec = self.env['estate.property'].browse(vals.get('property_id', False))
            property_rec.state = 'offer_received'
            if vals.get('price', 0) < property_rec.best_price:
                raise UserError(_("The new offer price must be higher than the current best offer %.2f." % property_rec.best_price))
        return super().create(vals_list)

    def action_accepted(self):
        accepted_offer = self.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')
        if accepted_offer:
            if self.price > accepted_offer.price:
                accepted_offer.status = 'refused'
                self.status = 'accepted'
                self.property_id.state = "offer_accepted"
                self.property_id.buyer_id = self.partner_id
                self.property_id.selling_price = self.price
            else:
                raise UserError(_("A higher or equal offer has already been accepted. You cannot accept this offer."))
        else:
            self.status = 'accepted'
            self.property_id.state = "offer_accepted"
            self.property_id.buyer_id = self.partner_id
            self.property_id.selling_price = self.price

    def action_refused(self):
        self.status = 'refused'
