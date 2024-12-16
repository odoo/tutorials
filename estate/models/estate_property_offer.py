from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date, timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offers'
    _order = 'price desc'

    price = fields.Float()
    partner_id = fields.Many2one('res.partner', string = 'Partner', required = True)
    property_id = fields.Many2one('estate.property', string = 'Property Name', required = True)
    status = fields.Selection(selection = [('refused', 'Refused'), ('accepted', 'Accepted')], copy = False)
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute = '_compute_deadline', inverse = '_compute_validity')
    property_type_id = fields.Many2one('estate.property.type', related = 'property_id.property_type_id', store = True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The offer price should be strictly positive'),
    ]

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = date.today() + timedelta(record.validity)

    def _compute_validity(self):
        for record in self:
            record.validity = (record.date_deadline - date.today()).days

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        price = vals.get('price')
        res = self.env['estate.property'].browse(property_id)
        if property_id and price:
            if res.exists():
                existing_offers = self.search([('property_id', '=', property_id), ('price', '>', price)])
                if existing_offers:
                    raise UserError('An offer with the higher price already exists.')
        if property_id:
            if res.exists():
                res.write({'state': 'offer_received'})
        return super(EstatePropertyOffer, self).create(vals)
    
    # @api.ondelete(at_uninstall = False)
    # def change_state(self):
    #     for record in self:
    #         if record.property_id.offer_ids == None:
    #             record.property_id.state = 'new'

    def action_accept(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                offer.status = 'refused'
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            record.property_id.state = 'new'
