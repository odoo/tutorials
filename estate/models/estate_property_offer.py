from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer object"
    _order = "price desc, validity desc"

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False, store=True, compute="_compute_status")
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    property_type_id = fields.Many2one('estate.property.type', related="property_id.property_type_id")

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    _positive_price = models.Constraint(
        'CHECK(price > 0)',
        'Price on offer must be positive',
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date.date(), days=record.validity) if record.create_date else fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days if record.create_date else (record.date_deadline - fields.Date.today()).days

    @api.depends("date_deadline")
    def _compute_status(self):
        for record in self:
            if not record.status and record.date_deadline < fields.Date.today():
                record.status = 'refused'

    def action_accept_offer(self):
        for record in self:
            if record.validity < 0:
                raise UserError(self.env._("Expired offer"))
            for offer in record.property_id.offer_ids:
                if offer.status == 'accepted':
                    raise UserError(self.env._("Only one offer can be accepted at a time"))
            for offer in record.property_id.offer_ids:
                offer.status = 'refused'
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    def action_refuse_offer(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.selling_price = 0.0
                record.property_id.buyer_id = False
            record.status = 'refused'
