from datetime import timedelta

from dateutil.utils import today

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Offer for a property"
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', "Accepted"), ('refused', "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_deadline',
        inverse='_inverse_deadline',
    )

    _check_price = models.Constraint('CHECK(price >= 0)', 'Price must be positive')

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for offer in self:
            offer.date_deadline = (offer.create_date or today()).date() + timedelta(
                days=offer.validity
            )

    def _inverse_deadline(self):
        for offer in self:
            offer.validity = (
                (offer.date_deadline - offer.create_date.date()).days
                if offer.create_date
                else (offer.date_line - today()).days
            )

    @api.model_create_multi
    def create(self, vals_list):
        for record in vals_list:
            property = self.env['estate.property'].browse(record['property_id'])

            if float_compare(property.best_price, record['price'], 2) == 1:
                raise UserError(_("You already have a higher offer"))

            if property.state == 'sold':
                raise UserError(
                    _("This property is already sold. You cannot add a new offer."),
                )

            property.state = 'offer_received'

        return super().create(vals_list)

    def action_accept(self):
        if self.property_id.state == 'cancelled':
            raise UserError(_("This property is cancelled."))
        if self.property_id.state == 'sold':
            raise UserError(_("This property is already sold."))

        self.status = 'accepted'
        self.property_id.state = 'offer_accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.selling_price = self.price

    def action_refuse(self):
        self.status = 'refused'
