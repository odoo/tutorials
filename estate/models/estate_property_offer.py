from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError

class estate_property_offer(models.Model):
    _name = 'estate.property.offer'
    _description = 'property offer'
    _sql_constraints = [
        ('offer_price_positive', 'CHECK(price >= 0)', 'An offer price must be strictly positive'),
    ]
    _order = 'price desc'

    price = fields.Float(string = 'price')
    status = fields.Selection([('accepted', 'Accepted'),('refused', 'Refused')], string = 'status')
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default = 7, string = "Validity (days)")
    date_deadline = fields.Date(string = "Deadline", compute = '_compute_date_deadline', inverse='_inverse_date_deadline',  store = True)
 
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                delta = record.date_deadline - fields.date.today()
                record.validity = delta.days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state in ('canceled', 'sold'):
                raise UserError("Cannot make changes on a canceled or sold property")
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
            record.property_id.state = 'offer_accepted'
            record.status = 'accepted'

    def action_refuse_offer(self):
        for record in self:
            if record.property_id.state in ('canceled', 'sold'):
                raise UserError("Cannot make changes on a canceled or sold property")
            record.status = 'refused'
    