from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'the offer of the property being sold'

    price = fields.Float()
    status = fields.Selection(selection = [('accepted', 'Accepted'), ('refused', 'Refused')], copy = False)
    partner_id = fields.Many2one('res.partner', string = 'Partner', required = True)
    property_id = fields.Many2one('estate.property', string = 'Property', required = True)
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute = '_compute_date_deadline', inverse = '_inverse_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days = record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                create_date = fields.Date.from_string(record.create_date)
                deadline_date = fields.Date.from_string(record.date_deadline)
                record.validity = (deadline_date - create_date).days

    def action_accept_offer(self):
        if self.property_id.buyer_id:
            raise UserError('This property already has an accepted offer')
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'
        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id
        return True

    def action_refuse_offer(self):
        if self.property_id.buyer_id == self.partner_id:
            self.property_id.buyer_id = False
            self.property_id.state = 'offer_received'
            self.property_id.selling_price = 0
        self.status = 'refused'
        return True

    _sql_constraints = [
        ('price_positive', 'CHECK(price > 0)', 'Price must be positive')
    ]