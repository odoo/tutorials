from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property offer for each property.'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', "Accepted"), ('refused', "Refused")], copy=False
    )
    partner_id = fields.Many2one(
        'res.partner', string="Partner", required=True)
    property_id = fields.Many2one(
        'estate.property', string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_date_deadline', inverse='_inverse_date_deadline'
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
        store=True
    )

    _check_price = models.Constraint(
        'CHECK(price >= 0)',
        "The Offer price cannot be negative."
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date or fields.Date.today()) + \
                timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (
                record.date_deadline -
                (record.create_date.date() or fields.Date.today())
            ).days

    def action_accepted(self):
        offers = self.property_id.offer_ids.filtered(
            lambda a: a.id != self.id)
        for offer in offers:
            offer.status = 'refused'
        self.status = 'accepted'
        self.property_id.partner_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'

    def action_refused(self):
        if self.status == 'accepted':
            self.property_id.partner_id = None
            self.property_id.selling_price = None
            self.property_id.state = 'offer_received'
        self.status = 'refused'

    # @api.ondelete(at_uninstall=False)
    # def _ondelete_offer(self):
    #     accepted_records = self.filtered(lambda a: a.status == 'accepted')
    #     if accepted_records:
    #         raise UserError(_("Accepted offer cannot be deleted."))

    @api.model
    def create(self, vals):
        for val in vals:
            price = val.get('price')
            property_id = val.get('property_id')
            property = self.env['estate.property'].browse(property_id)
            if property.state == 'new':
                property.best_price = price
            elif float_compare(price, property.best_price, precision_rounding=0.01) < 0:
                raise UserError(
                    _("Price should be greater than %s", property.best_price))
            else:
                property.best_price = price
            if property and property.state == 'new':
                property.state = 'offer_received'

        return super().create(vals)
