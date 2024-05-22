# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real Estate property offers"
    _order = 'price desc'
    _sql_constraints = [('positive_price', 'CHECK(price > 0)', "Price must be strictly positive.")]

    price = fields.Float("Price")
    status = fields.Selection(
        [
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(
        'Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline'
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Property Type",
        related='property_id.property_type_id',
        store=True,
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            date_deadline = record.date_deadline or fields.Date.today()
            create_date = fields.Date.to_date(record.create_date) or fields.Date.today()
            record.validity = (date_deadline - create_date).days

    @api.model
    def create(self, vals):
        model = self.env['estate.property']
        property_id = vals['property_id']
        property_model = model.browse(property_id)

        if property_model.state == 'sold':
            raise UserError(_("Cannot create a new offer for an already sold property."))

        if property_model.state == 'canceled':
            raise UserError(_("Cannot create a new offer for a canceled property."))

        if any(
            float_compare(offer.price, vals['price'], precision_rounding=0.01) > 0
            for offer in property_model.offer_ids
        ):
            raise UserError(_("An offer with a higher price already exists."))

        property_model.state = 'offer_received'
        return super().create(vals)

    def action_accept(self):
        for record in self:
            property_model = self.property_id
            if property_model.state == 'sold':
                raise UserError(_("Cannot accept offer on already sold property."))
            if property_model.state == 'canceled':
                raise UserError(_("Cannot accept offer on canceled property."))

            other_offers = property_model.offer_ids.filtered(lambda offer: offer.id != record.id)
            other_offers.action_refuse(from_action_accept=True)

            record.status = 'accepted'
            property_model.state = 'offer_accepted'
            property_model.selling_price = record.price
            property_model.buyer_id = record.partner_id
        return True

    def action_refuse(self, from_action_accept=False):
        for record in self:
            if record.status == 'accepted':
                raise UserError(
                    _("This action would refuse an already accepted offer.")
                    if from_action_accept
                    else _("Cannot refuse an already accepted offer.")
                )
            record.status = 'refused'
        return True
