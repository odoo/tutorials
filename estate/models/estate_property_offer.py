from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', "Accepted"), ('refused', "Refused")], copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        "Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline'
    )
    _offer_price_check = models.Constraint(
        'CHECK(price >= 0)', "Offer price should be strictly positive"
    )
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', store=True)

    # DEPENDS DECORATOR
    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date or fields.Datetime.today(
            )) + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline -
                               record.create_date.date()).days

    # BUTTON ACTION - OFFER
    def action_accept(self):
        if self.property_id.state == 'offer_accepted':
            raise UserError(
                _("An offer has already been accepted for this property.")
            )

        other_offer = self.property_id.offer_ids - self
        other_offer.write({'status': 'refused'})
        self.write({'status': 'accepted'})
        for offer in self:
            offer.property_id.write({
                'buyer_id': offer.partner_id.id,
                'selling_price': offer.price,
                'state': 'sold',
                'active': False
            })

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            record.property_id.write({
                'buyer_id': None,
                'selling_price': None,
            })

    # MODEL_CREATE_MULTI DECORATOR
    @api.model_create_multi
    def create(self, vals_list):
        if not vals_list:
            return super().create(vals_list)
        property_id = vals_list[0].get('property_id')
        if not property_id:
            return super().create(vals_list)

        # max_new_price = max(vals.get('price', 0) for vals in vals_list)
        max_new_price = 0
        for vals in vals_list:
            price = vals.get('price', 0)
            if price > max_new_price:
                max_new_price = price

        max_dp_price = 0
        for offer in property_id.offer_ids:
            if offer.price > max_dp_price:
                max_dp_price = offer.price

        if max_new_price <= max_dp_price:
            raise UserError(
                'Offer price should be greater then the existing one!')
        # result = self.env['estate.property.offer']._read_group(
        #     [('property_id', '=', property_id)],
        #     [],
        #     ['price:max']
        # )
        # # result = [(max_price_from_db),]
        # # result[0] = (max_price_form_db,)
        # # result[0][0] = max_price_from_db
        # max_db_price = result[0][0] if result else 0.0

        # if max_new_price <= max_db_price:
        #     raise UserError(
        #         "Offer price should be higher than the existing one!"
        #     )
        self.env['estate.property'].browse(
            property_id).state = 'offer_received'
        return super().create(vals_list)
