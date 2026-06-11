from dateutil.relativedelta import relativedelta

from odoo import api, fields, models # pylint: disable=import-error
from odoo.exceptions import UserError # pylint: disable=import-error
from odoo.exceptions import ValidationError # pylint: disable=import-error


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        'res.partner',
        required=True,
    )
    property_id = fields.Many2one(
        'estate.property',
        required=True,
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        store=True,
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = (
                    record.create_date.date()
                    + relativedelta(days=record.validity)
                )
            else:
                record.date_deadline = (
                    fields.Date.today()
                    + relativedelta(days=record.validity)
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    delta = (
                        record.date_deadline
                        - record.create_date.date()
                    )
                    record.validity = delta.days
                else:
                    delta = (
                        record.date_deadline
                        - fields.Date.today()
                    )
                    record.validity = delta.days

    _check_price = models.Constraint(
        'CHECK(price>0)',
        'Price must be positive'
    )

    def action_confirm(self):
        for offer in self.property_id.offer_ids:
            if self != offer and offer.status == 'accepted':
                raise UserError("An offer is already accepted")
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True