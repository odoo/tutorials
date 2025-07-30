from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare

class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer to real estate properties"
    _order = "price desc"

    price = fields.Float('Price')
    date_deadline = fields.Date('Deadline', compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    validity = fields.Integer('Validity (days)',default=7)
    partner_id = fields.Many2one('res.partner','Partner',required=True)
    property_id = fields.Many2one('estate.property','Property',required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    status = fields.Selection(
        selection=[('accepted','Accepted'),('refused','Refused')],
        copy=False
    )

    _sql_constraints = [
        ('check_price_positive','CHECK(price >= 0.0)','The offer price should be positive.')
    ]

    @api.depends('property_id.create_date','validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.property_id.create_date:
                record.date_deadline = record.property_id.create_date.date() + relativedelta(days=record.validity)
            else:
                record.date_deadline = False
    
    def _inverse_date_deadline(self):
        for record in self:
            if record.property_id.create_date and record.date_deadline:
                delta = record.date_deadline - record.property_id.create_date.date()
                record.validity = delta.days
            else:
                record.validity = 0

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            property_id = vals.get('property_id')
            offer_price = vals.get('price')

            if not property_id and offer_price is None:
                raise UserError("Property and offer price are required.")

            property_record = self.env['estate.property'].browse(property_id)
            existing_offers = property_record.offer_ids

            if existing_offers:
                max_offer = max(existing_offers.mapped('price'))
                if offer_price <= max_offer:
                    raise UserError(f"New offer must be higher than the current maximum offer of {max_offer}.")

            property_record.write({'state': 'offer_received'})
        return super().create(vals)
    
    def accepted_offer(self):
        for record in self:
            if record.property_id.state not in ('offer_accepted','sold','cancelled'):
                if float_compare(record.price,record.property_id.expected_price*0.90, precision_digits=2) == -1:
                    raise ValidationError("The selling price mut be at least 90% of the expected price! You must reduce the expected price if you want to accept this offer")
                else:
                    record.status = 'accepted'
                    record.property_id.selling_price = record.price
                    record.property_id.partner_id = record.partner_id
                    record.property_id.state = "offer_accepted"
            else:
                raise UserError("You cannot accepted another offer")
        return True

    def refused_offer(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError("You cannot refused the offer")
            else:
                record.status = 'refused'
        return True 