from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property offer"
    _order = 'price desc'
    # _inherit = 'crm.lead'

    price = fields.Float(required=True)
    status = fields.Selection(
        [
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ],
        copy=False)

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)
    validity = fields.Integer(string="Validity (Days)", default=7)
    date_deadline = fields.Date(string="Date Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'Offer price must be  positive.'
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            starting_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = starting_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            starting_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - starting_date).days

    @api.constrains('partner_id', 'property_id')
    def _check(self):
        time = fields.Datetime.now() - timedelta(minutes=5)
        for record in self:
            offers = self.env['estate.property.offer'].search([
                ('partner_id', '=', record.partner_id.id),
                ('property_id', '=', record.property_id.id),
                ('create_date', '>=', time)
            ])
            if len(offers) >= 3:
                record.property_id.is_suspicious = True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            current_price = vals.get('price', 0.0)
            property_id = self.env['estate.property'].browse(vals['property_id'])
            for offer in property_id.offer_ids:
                if current_price < offer.price:
                    raise UserError("Offer Price cannot be less than previous offer prices")

        offers = super().create(vals_list)

        for i in offers:
            if i.property_id.state == 'new':
                i.property_id.state = 'offer_received'

        return offers

    def action_accept(self):
        for record in self:
            already_accepted = False
            for offer in record.property_id.offer_ids:
                if offer.status == 'accepted':
                    already_accepted = True
                (record.property_id.offer_ids - offer).status = 'refused'
            if already_accepted:
                raise UserError("Only one offer can be accepted")
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'

        # self.env['crm.stage'].create({
        #         'is_won':'t',
        #         'fold':'f',
        #     })

        # a= self.env['crm.stage'].search([('id', '=', 4)])
        #     # record.action_set_won()

        # self.env['crm.lead'].create({
        #         'name': 'mohit',
        #         'stage_id' :a.id,
        #         })

        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
