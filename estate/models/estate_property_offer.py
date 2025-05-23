from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyTag(models.Model):
    _name = "estate.property.offer"
    _description = "real esate properties offers"

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
            ('pending', 'Pending')
        ],
        copy=False,
        default='pending',
        required=True
    )
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)
    property_id = fields.Many2one('estate.property', 'Property', required=True)

    validity = fields.Integer('Validity (Days)', default=7)
    date_deadline = fields.Date('Deadline', compute="_compute_deadline", inverse="_inverse_deadline")

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'An offer price must be strictly positive!'),
    ]

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if not record.validity:
                record.date_deadline = False
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if not record.date_deadline:
                record.validity = 0
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_to_accept(self):
        for record in self:
            property_obj = record.property_id
            if property_obj.state in ["sold", "offer_accepted"]:
                raise UserError(_('Property already accepted an offer.'))
            record.status = 'accepted'
            property_obj.selling_price = record.price
            property_obj.partner_id = record.partner_id
            property_obj.state = 'offer_accepted'

            (property_obj.offer_ids - record).action_to_refuse()
        return True

    def action_to_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    def action_to_undo(self):
        for record in self:
            property_obj = record.property_id

            if record.status == 'accepted':
                property_obj.state = 'offer_received'
                property_obj.partner_id = False
                property_obj.selling_price = 0

            record.status = 'pending'
        return True

    @api.constrains('price')
    def _check_minimum_price(self):
        for record in self:
            expected_price = record.property_id.expected_price
            min_acceptable_price = expected_price * 0.9

            if float_compare(record.price, min_acceptable_price, precision_digits=2) < 0:
                raise ValidationError(
                    _(
                        "Offer rejected: The proposed price must be at least 90%% of the property's expected price "
                        "(minimum required: $%.2f)."
                    ) % min_acceptable_price
                )
