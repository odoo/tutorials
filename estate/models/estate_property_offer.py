from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"
    _order = "price desc"

    price = fields.Float()

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The Offer Price must be strictly positive'
    )

    status = fields.Selection(
        selection=[
            ('new', 'New'),
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
        default='new',
    )

    partner_id = fields.Many2one(comodel_name='res.partner', required=True)

    property_id = fields.Many2one(comodel_name='estate.property', required=True)

    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    validity = fields.Integer(string='Validity (days)', default=7)

    date_deadline = fields.Date(string='Deadline', compute='_compute_deadline', inverse='_inverse_total')

    def _get_create_date(self, record):
        return fields.Date.to_date(record.create_date) or fields.Date.today()

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = self._get_create_date(record) + relativedelta(days=record.validity)

    def _inverse_total(self):
        for record in self:
            record.validity = (record.date_deadline - self._get_create_date(record)).days

    def action_accept(self):
        for record in self:
            if record.status == 'refused':
                raise UserError(self.env._("Cannout accept an offer that has been refused"))

            if not record.property_id._accept_offer(self):
                raise UserError(self.env._("Another offer is already accepted"))

            record.status = 'accepted'

        return True

    def action_refuse(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError(self.env._("Cannout refuse an offer that has been accepted"))

            record.status = 'refused'

        return True

    @api.model
    def create(self, vals_list):
        for val in vals_list:
            property = self.env['estate.property'].browse(val['property_id'])

            if property.state == "new":
                property.state = "received"

            price = val['price']
            max_price = property.offer_ids[0]['price'] if property.offer_ids else -1

            if max_price > price:
                raise UserError(self.env._("New offer price must be greater or equal than %d", max_price))

        return super().create(vals_list)
