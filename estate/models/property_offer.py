from odoo import api, fields, models, exceptions


class EstatePropertyOffer(models.Model):
    _name = 'estate_property_offer'
    _description = 'estate property offer'
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False, readonly=True)
    partner_id = fields.Many2one('res.partner', required=True, string='Partner')
    property_id = fields.Many2one('estate_property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_deadline', inverse='_inverse_deadline')
    property_type_id = fields.Many2one("estate_property_type", related="property_id.property_type_id", store=True, string="Property Type")

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date.date(), days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)  # If no create_date we take the date of today

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days  # If no create_date we take the date of today

    def action_status_accepted(self):

        if len(self) > 1:
            raise exceptions.UserError('Only one offer can be accepted')

        if self.status != 'accepted' and 'accepted' in self.mapped('property_id.property_offer_id.status'):
            raise exceptions.UserError('Another offer is already accepted')

        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id
        self.property_id.state = 'offer accepted'

    def action_status_refused(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.selling_price = False
                record.property_id.buyer = False
                record.property_id.state = 'offer received'
            record.status = 'refused'

    _check_offer_price = models.Constraint(
    'CHECK(0 < price)',
    'An offer price must be strictly positive')

    @api.model
    def create(self, vals_list):
        
        for vals in vals_list:
            max_existing_price = max((offer.price for offer in self.env['estate_property'].browse(vals_list[0]['property_id']).property_offer_id), default=0)
            if vals['price'] < max_existing_price:
                raise exceptions.UserError('The offer must be higher than ' + str(max_existing_price))

        return super().create(vals_list)
