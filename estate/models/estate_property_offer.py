from odoo import api, fields, models
from odoo.tools.date_utils import add
from odoo.exceptions import UserError
from odoo.tools.translate import _


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "estate properties offers"
    _sql_constraints = [
        (
            'check_strictly_positive_offer_price',
            'CHECK(price > 0)',
            "Offer Price must be strictly positive",
        ),
    ]

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        "Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline'
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = add(
                record.create_date or fields.Date.today(), days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (
                (record.date_deadline or fields.Date.today())
                - (fields.Date.to_date(record.create_date) or fields.Date.today())
            ).days

    def action_accept(self):
        for record in self:
            if state := self.property_id.state in ('sold', 'canceled'):
                raise UserError(_(f'Can\'t accept offer on {state} estate'))

            self.property_id.offer_ids.filtered(lambda o: o.id != record.id).update(
                {'status': 'refused'}
            )

            record.status = 'accepted'
            self.property_id.partner_id = record.partner_id
            self.property_id.selling_price = record.price

        return True

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError(_("Can\'t refuse accepted offer"))

            record.status = 'refused'

        return True
