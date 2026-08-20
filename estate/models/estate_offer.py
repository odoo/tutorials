from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class EstateOffer(models.Model):
    _name = 'estate.offer'
    _description = 'Estate Offer'

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    _check_price_positive = models.Constraint(
        "CHECK(price > 0)",
        "An offer price must be strictly positive.",
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date or fields.Date.today()) + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.write({
                'buyer_id': record.partner_id.id,
                'selling_price': record.price,
            })

        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'

        return True
