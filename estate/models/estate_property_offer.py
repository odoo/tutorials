from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy="False",
        help="Status of the Offer")
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
        help='Person making the offer'
    )
    property_id = fields.Many2one(
        'estate.property',
        string='Property ID',
        required=True
    )
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(
        string='Deadline',
        compute='_compute_deadline',
        inverse='_inverse_deadline'
    )

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = ((record.create_date) + relativedelta(days=record.validity)).date()
            elif record.validity:
                record.date_deadline = (fields.Datetime.now() + relativedelta(days=record.validity)).date()
            else:
                record.date_deadline = False

    @api.depends("create_date", "date_deadline")
    def _inverese_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date).days
            else:
                record.validity = 0

    def action_accept_button(self):
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = 'offer accepted'

    def action_refuse_button(self):
        self.status = 'refused'
        self.property_id.selling_price = 0
        self.property_id.buyer_id = ''
