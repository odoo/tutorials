from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'
    _order = 'price desc'

    price = fields.Float(string="Price")
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        string="Status",
    )
    partner_id = fields.Many2one(
        'res.partner', string="Partner", required=True
    )
    property_id = fields.Many2one(
        'estate.property', string="Property", required=True
    )
    validity = fields.Integer(default=7, string="Validity (Days)")
    date_deadline = fields.Date(
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
        string='Deadline',
    )
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', store=True
    )

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        "The offer price of must be strictly positive!"
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + \
                    relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline -
                               fields.Date.to_date(record.create_date)).days

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            related_property = self.env['estate.property'].browse(
                vals['property_id'])
            if related_property.state in ['sold', 'canceled', 'offer_accepted']:
                raise ValidationError(self.env._(
                    "You cannot make an offer on a sold or canceled property!")
                )
            for offer in related_property.offer_ids:
                if offer.price > vals['price']:
                    raise UserError(self.env._("This offer price is lower than the current ones"))

        return super().create(vals_list)

    def action_accept_offer(self):
        for record in self:
            if record.status == 'accepted':
                continue
            for offer in record.property_id.offer_ids:
                if offer.status == 'accepted':
                    offer.status = 'refused'
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
