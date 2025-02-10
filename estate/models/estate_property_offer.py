from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'

    price = fields.Float(string="price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
        ],string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity (Days)', default=7)
    deadline_date = fields.Date(string='Deadline', compute='_compute_deadline_date', inverse='_inverse_deadline_date')        

    @api.depends('create_date', 'validity')
    def _compute_deadline_date(self):
        for record in self:
            if record.create_date:
                record.deadline_date = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.deadline_date = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            record.validity = (record.deadline_date - record.create_date.date()).days if record.deadline_date else 0

    def action_order_accepted(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            for offer in record.property_id.offer_ids:
                if offer.id is not record.id:
                    offer.status = 'refused'

    def action_order_refused(self):
        for record in self:
            record.status = 'refused'
            record.property_id.selling_price = 0
     