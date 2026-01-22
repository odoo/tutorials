from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

OFFER_STATUS = [
    ('accepted', 'Accepted'),
    ('refused', 'Refused'),
]


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An estate property offer model"

    # === FIELDS ===#

    price = fields.Float()
    status = fields.Selection(
        selection=OFFER_STATUS,
        copy=False)
    partner_id = fields.Many2one(
        "res.partner",
        string='Partner',
        required=True)
    property_id = fields.Many2one(
        "estate.property",
        string='Property',
        required=True)
    validity = fields.Integer(
        default=7,
        string='Validity (days)')
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        string='Deadline')

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The price must be strictly positive!',
    )

    # === COMPUTE METHODS ===#

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + \
                    relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Datetime.today() + \
                    relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days

    # === ACTION METHODS ===#

    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_reject_offer(self):
        for record in self:
            record.status = 'refused'
        return True
