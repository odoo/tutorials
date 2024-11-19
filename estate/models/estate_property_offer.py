from odoo import fields, models, api, _
from datetime import timedelta, date
from odoo.exceptions import UserError


class EstatePropertyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False, readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', required=True, ondelete="cascade")
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse='_inverse_deadline', string='Deadline')
    property_type_id = fields.Many2one(related="property_id.estate_property_type_id")

    @api.depends("validity", 'create_date')
    def _compute_deadline(self):
        for record in self:
            creation_date = record.create_date or fields.Datetime.now()
            record.date_deadline = creation_date + timedelta(days=record.validity)
        return True

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - date.today()).days
        return True

    def action_accept_offer(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError(_('Already accepted offer: ' + record.property_id.title + ', Partner: ' + record.partner_id.name))
            record.property_id.offer_ids.update({'status':'refused'})
            record.property_id.update({'selling_price':record.price, 'buyer_id':record.partner_id, 'state':'offer_accepted'})

        record.status = "accepted"
        return True

    def action_refuse_offer(self):
        not_accepted_records = self.filtered(lambda record: record.status == 'refused')
        if not_accepted_records:
            message = ''.join(['Already refused offer Property:' + offer.property_id.title + ', Partner: ' + offer.partner_id.name + '\n' for offer in not_accepted_records])
            raise UserError(_(message))
        self.status = "refused"
        self.property_id.update({'selling_price':0, 'buyer_id':False, 'state':'new'})
        return True
    
    @api.model
    def create(self, vals):
        property = self.env['estate.property'].browse(vals['property_id'])

        if property.offer_ids and len(property.offer_ids) > 0 and any(offer.price > vals['price'] for offer in property.offer_ids):
            raise UserError(_("Can't place an offer with less price than existing offers"))
        return super().create(vals)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         _('The offer price must be strictly positive.')),
    ]
