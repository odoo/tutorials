from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Offer Property Model"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True
    )

    _sql_constraint = [
        ('check_offer_price', 'check(price > 0.0)', 'The offer price must be greater than 0')
    ]

    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            record.property_id.buyer = record.partner_id
            rejected_offers = self.search([
                ('property_id', '=', record.property_id.id), ('id', '!=', record.id)
            ])
            rejected_offers.write({'status':'rejected'})

    def action_reject_offer(self):
        for record in self:
            record.status = 'rejected'
            if record.property_id.buyer == record.partner_id:
                record.property_id.buyer = False

    @api.depends("create_date","validity")
    def _compute_deadline_date(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 7

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if 'property_id' in vals:
                property_rec = self.env['estate.property'].browse(vals['property_id'])
                existing_offers = property_rec.mapped('offer_ids.price')
                if existing_offers and vals.get('price') < max(existing_offers):
                    raise UserError("Cannot create an offer because of amount lower than existing offers.\n"
                                    f"Highest existing offer: {max(existing_offers)}"
                    )
                property_rec.write({
                    'state': 'offer_received'
                })
        return super().create(vals_list)
