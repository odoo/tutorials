from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection(string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Datetime('Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', string='Property Type', store=True)

    _estate_property_offer_check_price = models.Constraint('CHECK(price > 0)', 'Price must be strictly positive.')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            reference_date = record.create_date if record.create_date else fields.Datetime.now()
            record.date_deadline = reference_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - fields.Datetime.now()).days

    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            record.property_id.buyer_id = record.partner_id
            offer_ids = record.property_id.offer_ids
            (offer_ids - record).status = 'refused'

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
