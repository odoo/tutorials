from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', "Accepted"),
            ('refused', "Refused"),
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
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True)
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
                    record.create_date.date() + relativedelta(days=record.validity)
                )
            else:
                record.date_deadline = (
                    fields.Date.today() + relativedelta(days=record.validity)
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    delta = (
                        record.date_deadline - record.create_date.date()
                    )
                    record.validity = delta.days
                else:
                    delta = (
                        record.date_deadline - fields.Date.today()
                    )
                    record.validity = delta.days

    _check_price = models.Constraint(
        'CHECK(price>0)', 'Price must be positive')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            current_price = vals.get('price')
            property_id = self.env['estate.property'].browse(
                vals['property_id'])
            for offer in property_id.offer_ids:
                if current_price < offer.price:
                    raise UserError(
                        "The offer must be higher than the current highest offer.")
        offers = super().create(vals_list)
        for record in offers:
            if record.property_id.state == 'new':
                record.property_id.state = 'offer_received'
        return offers

    def action_confirm(self):
        for offer in self.property_id.offer_ids:
            if self != offer and offer.status == 'accepted':
                raise UserError(_("An offer is already accepted."))
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
