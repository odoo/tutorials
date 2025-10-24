from odoo import fields, models, api
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer for the property'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True, default=lambda self: self.env.user)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _offer_price_strictly_positive = models.Constraint(
        'CHECK(price > 0)',
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Datetime.now() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            deadline = datetime(record.date_deadline.year, record.date_deadline.month, record.date_deadline.day)
            record.validity = int((deadline - fields.Datetime.now()).days)

    def accept_offer(self):
        for record in self:
            if not record.property_id.offer_accepted:
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer = record.partner_id
                record.property_id.state = 'offer accepted'
                record.property_id.offer_accepted = True
            else:
                raise UserError("Can not accept more than one offer")

    def reject_offer(self):
        for record in self:
            record.status = 'refused'

    @api.model
    def create(self, vals_list):
        if len(vals_list) > 0:
            if len(self.env['estate.property'].browse(vals_list[0].get('property_id')).offer_ids.mapped('price')) and vals_list[0].get('price') < min(self.env['estate.property'].browse(vals_list[0].get('property_id')).offer_ids.mapped('price')):
                raise UserError("Can not have an offer that is less the minimum offer")
            self.env['estate.property'].browse(vals_list[0]['property_id']).state = 'offer received'
        return super().create(vals_list)
