from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"
    _order = 'price desc'

    price = fields.Float('Price')
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one('estate.property.type', compute='_compute_property_type_id', store='True')

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'price must be positive'),
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = fields.Datetime.today()
            if record.create_date:
                create_date = record.create_date
            record.date_deadline = create_date + relativedelta(days=record.validity)

    @api.depends('property_id')
    def _compute_property_type_id(self):
        for record in self:
            if record.property_id and record.property_id.property_type_id:
                record.property_type_id = record.property_id.property_type_id

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        if self.property_id.partner_id:
            raise UserError('Only one offer can be accepted')
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id
        self.property_id.state = 'offer_accepted'

    def action_reject_offer(self):
        if self.status == 'accepted':
            self.property_id.selling_price = 0
            self.property_id.partner_id = ''
        self.status = 'refused'

    def unlink(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.selling_price = 0
                record.property_id.partner_id = ''
                record.property_id.state = 'new'
        return super().unlink()
