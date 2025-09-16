from odoo import api, fields, models


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Offer"
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection([('accepted', "Accepted"), ('refused', "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date('Validity Date', compute='_compute_date_deadline', inverse='_compute_validity')
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store=True)

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _compute_validity(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        self.status = 'refused'
        return True

    _offer_price_positive = models.Constraint('CHECK(price > 0)', "The offer price must be positive.")
