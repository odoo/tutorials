from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import timedelta


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
            record.validity = (record.date_deadline - create_date.date()).days
