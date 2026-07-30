from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        selection=[
                ('accepted', "Accepted"),
                ('refused', "Refused")
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )
    property_type_id = fields.Many2one(
        'estate.property.type',
        related='property_id.property_type_id',
        store=True,
    )

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        "An offer price must be strictly positive",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])

            if property.offer_ids:
                max_offer = property.offer_ids[0].price
                if float_compare(vals['price'], max_offer, precision_digits=2) <= 0:
                    raise UserError(self.env._("The offer must be strictly higher than %.2f", max_offer))

            property.state = 'offer_received'

        return super().create(vals_list)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - fields.Date.to_date(create_date)).days

    def action_accept_offer(self):
        for record in self:
            if record.status:
                raise UserError(
                    self.env._("You can't accept an offer that has already been accepted/refused")
                )

            record.status = 'accepted'

            other_offers = record.property_id.offer_ids - record
            other_offers.write({'status': 'refused'})

            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

            record.property_id.state = 'offer_accepted'

        return True

    def action_refuse_offer(self):
        for record in self:
            if record.status:
                raise UserError(
                    self.env._("You can't refuse an offer that has already been accepted/refused")
                )
            record.status = 'refused'

        return True
