from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate property offer module'
    _order = 'price desc'

    name = fields.Char(required=True)
    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )

    validity = fields.Integer(default=7)
    create_date = fields.Date(default=fields.Date.today(), readonly=True)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_compute_inverse_deadline')

    partner_id = fields.Many2one(comodel_name='res.partner', required=True)
    property_id = fields.Many2one(comodel_name='estate.property', required=True)
    property_type_id = fields.Many2one(comodel_name='estate.property.type', related='property_id.estate_type_id')

    _sql_constraints = [
        ('check_stricly_positive_price', 'CHECK(price > 0)',
         'The price of an estate property offer must be strictly positive.'),
    ]

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(days=record.validity)

    def _compute_inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    def action_accepted(self):
        if self.status == 'accepted':
            return

        if any(offer.status == 'accepted' for offer in self.property_id.estate_offer_ids):
            raise exceptions.UserError('You can only accept one offer')

        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id
        if self.status != 'sold':
            self.property_id.status = 'offer accepted'

    def action_refused(self):
        if self.status == 'refuse':
            return

        if self.status == 'accepted':
            self.property_id.selling_price = 0
            self.property_id.partner_id = None

        self.status = 'refused'
