from odoo import api, fields, models
from odoo.tools.date_utils import add
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.tools.float_utils import float_compare


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
    _order = 'price desc'

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
    property_type_id = fields.Many2one(
        'estate.property.type',
        string="Property Type",
        related='property_id.property_type_id',
        store=True,
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
            if (state := self.property_id.state) in ('sold', 'canceled'):
                raise UserError(_('Can\'t accept offer on %s estate') % state)

            self.property_id.offer_ids.filtered(lambda o: o.id != record.id).update(
                {'status': 'refused'}
            )

            record.status = 'accepted'
            self.property_id.state = 'offer_accepted'
            self.property_id.partner_id = record.partner_id
            self.property_id.selling_price = record.price

        return True

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError(_("Can\'t refuse accepted offer"))

            record.status = 'refused'

        return True

    @api.model
    def create(self, vals):
        estate_property = self.env['estate.property'].browse(vals['property_id'])
        if any(
            float_compare(offer.price, vals['price'], precision_rounding=0.1) > 0
            for offer in estate_property.offer_ids
        ):
            raise UserError(_('Can\'t create an offer with a lower amount than existing offer'))

        if estate_property.state == 'new':
            estate_property.state = 'offer_received'

        return super().create(vals)
