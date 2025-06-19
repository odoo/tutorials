from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real estate property offer"
    _order = 'price DESC'
    _sql_constraints = [
        ('check_positive_offer_price', 'CHECK(price > 0)',
         "The property's offer price must be positive."),
    ]

    property_id = fields.Many2one(comodel_name='estate.property', required=True)
    price = fields.Float()
    status = fields.Selection(selection=[('accepted', "Accepted"), ('refused', "Refused")], copy=False)
    partner_id = fields.Many2one(comodel_name='res.partner', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)
    validity = fields.Integer()
    date_deadline = fields.Date(compute='_compute_date_deadline_from_validity', inverse='_inverse_validity_from_deadline')

    def _inverse_validity_from_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.today()).days if offer.date_deadline else 0.0

    @api.depends('validity')
    def _compute_date_deadline_from_validity(self):
        for offer in self:
            offer.date_deadline = (offer.create_date or fields.Date.today()) + relativedelta(days=offer.validity)

    @api.model_create_multi
    def create(self, values_list):
        property_ids = [offer['property_id'] for offer in values_list]
        properties = {property.id: property for property in self.env['estate.property'].browse(property_ids)}
        for offer in values_list:
            property = properties[offer['property_id']]
            max_offer_price = max(property.offer_ids.mapped('price'), default=0.0)
            if max_offer_price > offer.get('price', 0):
                raise ValidationError(_("There is a better price for this property already!"))
            property.state = 'received'
        return super().create(values_list)

    def accept_offer(self):
        for offer in self:
            offer.status = 'accepted'
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price

            if len(offer.property_id.offer_ids.filtered(lambda r: r.status == 'accepted')) > 1:
                raise UserError(_("You can't Accept more than one offer"))

        return True

    def refuse_offer(self):
        for offer in self:
            offer.status = 'refused'
