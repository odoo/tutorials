from odoo import api, fields, models
from datetime import date, timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property offer Model"
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity(days)', default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_deadline', string='Deadline')
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id',
                                       string='Property Type', store=True)

    _sql_constraints = [
        ('check_offer_price_positive', 'CHECK(price > 0)', 'Offer price must be positive!'),
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.validity:
                record.date_deadline = date.today() + timedelta(days=record.validity)
            else:
                record.date_deadline = False

    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - date.today()).days
            else:
                record.validity = 7

    def action_accept_offer(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError("This offer has already been accepted.")
            check_other_accepted = self.search([
                ('property_id', '=', record.property_id.id),
                ('status', '=', 'accepted')
            ])
            if check_other_accepted:
                raise UserError("Another offer has already been accepted for this property.")
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id
            record.property_id.state = 'accepted'
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
            check_other_accepted = self.search([
                ('status', '=', 'accepted')
            ])
            if not check_other_accepted:
                record.property_id.selling_price = 0
                record.property_id.partner_id = False
        return True

    @api.ondelete(at_uninstall=False)
    def _reset_selling_price(self):
        for offer in self:
            if offer.status == 'accepted':
                offer.property_id.selling_price = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            price = vals.get('price', 0.0)
            if property_id:
                property_obj = self.env['estate.property'].browse(property_id)
                best_price = property_obj.best_price or 0.0
                if price < best_price:
                    raise UserError("Offer price must be greater than or equal to the best offer price.")
        records = super().create(vals_list)
        for record in records:
            if record.partner_id:
                record.property_id.state = 'received'
        return records
