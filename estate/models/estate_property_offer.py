from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Offer"
    _order = 'price desc'
    _price_check = models.Constraint('CHECK(price > 0)', "The offer price must be strictly positive.")

    price = fields.Float()
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', string="Property Type", store=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    status = fields.Selection(
        selection=[('accepted', "Accepted"), ('refused', "Refused")],
        copy=False
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(start_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    @api.model_create_multi
    def create(self, vals_list):
        property_ids = [vals['property_id'] for vals in vals_list if vals.get('property_id')]
        properties = self.env['estate.property'].browse(property_ids)
        property_map = {prop.id: prop for prop in properties}

        for vals in vals_list:
            prop = property_map.get(vals.get('property_id'))
            if prop:
                if prop.offer_ids:
                    max_offer = max(prop.offer_ids.mapped('price'), default=0)
                    if vals.get('price', 0) < max_offer:
                        raise UserError(self.env._("The offer must be higher than existing offers!"))
                prop.state = 'offer_received'

        return super().create(vals_list)

    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True
