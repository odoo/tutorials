from odoo import fields, models, api
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property ofer"

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
    )
    partner_id = fields.Many2one("res.users", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string='Offer Validity', default=7)
    date_deadline = fields.Date('Offer Deadline', compute='_compute_validity', inverse='_inverse_validity')

    @api.depends('validity', 'create_date')
    def _compute_validity(self):
        for record in self:
            if record.create_date:
                create_date = record.create_date
            else:
                create_date = fields.Date.today()
            record.date_deadline = create_date + relativedelta(days=record.validity)

    @api.onchange("date_deadline")
    def _inverse_validity(self):
        for record in self:
            if record.create_date:
                create_date = record.create_date
            else:
                create_date = fields.Date.today()
            # record.validity = (record.date_deadline - create_date).days
            create_date_val = create_date.date() if hasattr(create_date, 'date') else create_date
            record.validity = (record.date_deadline - create_date_val).days
    
    def action_accept(self):
        for record in self:
            if record.property_id.state == 'sold':
                odoo.exceptions.UserError('Property was already sold')
            if record.property_id.state == 'cancelled':
                odoo.exceptions.UserError('Cancelled properties cannot be sold')
            else:
                record.status = 'accepted'
                record.property_id.state = 'sold'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
