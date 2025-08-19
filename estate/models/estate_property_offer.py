from dateutil.relativedelta import relativedelta
from datetime import date

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for properties"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True, ondelete='cascade')
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ('positive_offer_price', 'CHECK(price > 0)', 'Offer price must be greater than zero!')
    ]

#-------------compute date using validity days-----------------------#
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline =  record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = date.today() + relativedelta(days=record.validity)

#------------compute validity days from date-------------------------#
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days

#-------------at time compute validity days---------------------------#
    @api.onchange('date_deadline')
    def _onchange_date_deadline(self):
        self._inverse_date_deadline()

#--------------on click offer accept button----------------------------#
    def action_offer_accept_button(self):
        for record in self:
            if record.status != 'accepted' and record.property_id.selling_price == 0:
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.state = 'offer_accepted'
        return True

#--------------on click offer refuse button---------------------------#
    def action_offer_refuse_button(self):
        for record in self:
            if record.status == 'accepted':
                record.status = 'refused'
                record.property_id.selling_price = 0.0
                record.property_id.buyer_id = False
                record.property_id.state = 'offer_received'
            else:
                record.status = 'refused'
        return True

#---------------before create offer check the offer is bigger than other offer-----------------------#
    @api.model_create_multi
    def create(self, vals_list):
        property_obj = self.env['estate.property'].browse(vals_list[0]['property_id'])
        if property_obj.state == 'sold':
            raise UserError(_("Cannot create an offer for a sold property."))
        prices = [val['price'] for val in vals_list]
        min_price = min(prices, default=property_obj.best_price)
        if min_price < property_obj.best_price:
            raise UserError(_("offer with a lower amount than an existing offer"))
        property_obj.state = 'offer_received'

        return super().create(vals_list)
