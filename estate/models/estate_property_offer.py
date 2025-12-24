from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Offer to buy real estate property"
    _order = 'price desc'

    property_id = fields.Many2one(
        'estate.property',
        string="Property Name",
        required=True,
        ondelete='cascade',
    )
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    create_date = fields.Date(default=lambda self: fields.Date.today())
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        "Deadline",
        compute='_compute_date',
        inverse='_inverse_date',
    )
    @api.depends('validity')
    def _compute_date(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(days=record.validity)

    def _inverse_date(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days

    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id.id)
    price = fields.Monetary("Price")
    status = fields.Selection(
        string="Status",
        selection=[('accepted', "Accepted"), ('refused', "Refused")],
        copy=False,
    )
    def accept_offer(self):
        for record in self:
            if record.property_id.offer_ids.filtered(lambda o: o.status == 'accepted'):
                raise UserError(record.env._("There is already an accepted offer for this property."))
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            record.property_id.buyer_id = record.partner_id
        return True
    def refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        "The offer price must be positive",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'property_id' in vals and 'price' in vals:
                linked_property = self.env['estate.property'].browse(vals['property_id'])
                if linked_property.best_offer and vals['price'] < linked_property.best_offer:
                    raise UserError("The offer price must be higher than the current best offer of %.2f" % property.best_offer)
        return super().create(vals_list)

    @api.constrains('status')
    def _check_fair_price(self):
        for record in self:
            if record.status == 'accepted' and record.price < record.property_id.expected_price*0.9:
                raise ValidationError(record.env._(f"The selling price must be at least {90}% of the expected price. \n If you want to accept this offer, lower the expected price."))
