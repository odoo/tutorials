from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"

    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False
    )

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for rec in self:
            create_date = rec.create_date or fields.Datetime.now()
            rec.date_deadline = fields.Date.add(create_date, days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            create_date = rec.create_date or fields.Datetime.now()
            rec.validity = (rec.date_deadline - create_date.date()).days

    def action_accept(self):
        for rec in self:
            if rec.property_id.state == 'sold':
                raise UserError(_('This property is already sold.'))
            rec.status = 'accepted'
            rec.property_id.state = 'sold'
            rec.property_id.buyer_id = rec.partner_id
            rec.property_id.selling_price = rec.price
        return True

    def action_reject(self):
        for rec in self:
            old_record_status = rec.status
            rec.status = 'refused'
            if old_record_status == 'accepted':
                rec.property_id.state = 'offer_received'
                rec.property_id.buyer_id = False
                rec.property_id.selling_price = 0.0
        return True

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offer price must be strictly positive!'),
    ]

    @api.model
    def create(self, vals_list):
        property_id = vals_list.get('property_id')
        price = vals_list.get('price')

        property_record = self.env['estate.property'].browse(property_id)
        if property_record.best_price >= price:
            raise UserError(_(f"The offer price must be higher than {property_record.best_price}"))

        property_record.state = 'offer_received'

        return super(EstatePropertyOffer, self).create(vals_list)

