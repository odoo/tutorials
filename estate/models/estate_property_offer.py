from odoo import fields,models,api
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta

class EstatePropertytOffer(models.Model):
    _name = "estate.property.offer"
    _description ="It defines the estate property Offer"
    _order="price desc"

    price= fields.Float(copy=False, string='Price')
    status= fields.Selection(selection=[('Accepted','Accepted'), ('Refused','Refused')], string='Status', copy=False)
    partner_id= fields.Many2one('res.partner', string="Partner", required=True)

    property_id= fields.Many2one('estate.property', string='Property',required=True)
    validity= fields.Integer(default=7)
    date_deadline= fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    property_type_id = fields.Many2one(string="Property Type",related='property_id.property_type_id',store=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        for record in records:
            property_record = record.property_id
            existing_offers = property_record.offer_ids

            min_existing_price = min(existing_offers.mapped('price'), default=0)

            if record.price < min_existing_price:
                raise UserError(
                    f"The offer price ({record.price}) must be higher than the minimum of existing offer ({min_existing_price})."
                )

            if property_record.state == 'new':
                property_record.write({'state': 'offer_received'})

        return records

    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date=record.create_date or fields.Datetime.today()
            record.date_deadline= create_date.date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date= record.create_date or fields.Datetime.today()
            record.validity=(record.date_deadline-create_date.date()).days

    def action_accept(self):
        for record in self:
            if record.property_id.buyer_id:
                raise UserError("An offer has already been accepted for this property.")

            record.status = 'Accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'

    def action_reject(self):
        for record in self:
            record.status = 'Refused'
