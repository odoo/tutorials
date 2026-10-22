from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(required=True)
    status = fields.Selection(selection=[('pending', 'Pending'), ('accepted', 'Accepted'), ('refused', 'Refused')], required=True, default="pending")
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Datetime.now()
            record.date_deadline = fields.Date.add(base_date.date(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            base_date = (record.create_date or fields.Datetime.now()).date()
            deadline_date = record.date_deadline or base_date
            record.validity = (deadline_date - base_date).days

    def action_accept(self):
        for record in self:
            accepted_offers = record.property_id.offer_ids.filtered(lambda offer: offer.status == 'accepted')
            if accepted_offers:
                raise UserError("There is already an accepted offer for this property")
            
            other_offers = record.property_id.offer_ids - record
            other_offers.write({'status': 'refused'})

            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

            return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

