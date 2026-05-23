from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
        copy=True
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        required=True
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Property",
        required=True
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
    )
    quotation_id = fields.Many2one(
        "sale.order",
        string="Quotation",
        readonly=True,
        copy=False
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_set_date_deadline",
    )
    is_suspicious = fields.Boolean(
        string="Suspicious",
        default=False,
        readonly=True,
        copy=False,
        compute="_compute_is_suspicious",
        store=True,
    )

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'Offer price must be strictly positive!',
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(
                    record.create_date,
                    days=record.validity,
                )
            else:
                record.date_deadline = fields.Date.add(
                    fields.Date.today(),
                    days=record.validity,
                )

    def _set_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (
                    record.date_deadline -
                    record.create_date.date()
                ).days

    @api.depends("partner_id", "create_date")
    def _compute_is_suspicious(self):
        for record in self:
            if not record.create_date:
                record.is_suspicious = False
                continue

            start = (record.create_date - timedelta(minutes=5))
            end = (record.create_date + timedelta(minutes=5))
            recent_offers = self.search([
                ('partner_id', '=', record.partner_id.id),
                ('create_date', '>=', start),
                ('create_date', '<=', end),
            ])

            record.is_suspicious = len(recent_offers) >= 3

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(
                vals.get('property_id', False)
            )
            if property_id.offer_ids:
                max_offer = max(property_id.offer_ids.mapped('price'))
                if vals.get('price', 0) < max_offer:
                    raise UserError(
                        "You cannot create an offer lower "
                        "than an existing offer of %.2f" % max_offer
                    )

            property_id.state = 'offer_received'

        return super().create(vals_list)

    def action_accept(self):
        for record in self:
            accepted_offer = record.property_id.offer_ids.filtered_domain([
            ("status", "=", "accepted"),
            ("id", "!=", record.id),
        ])
            if accepted_offer:
                raise UserError("An offer has already been accepted for this property.")
            record.property_id.write({
                'buyer_id': record.partner_id.id,
                'selling_price': record.price,
                'state': 'offer_accepted',
        })

            for offer in record.property_id.offer_ids:
                if offer.id != record.id:
                    offer.status = "refused"
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    def _cron_automatic_refuse(self):
        today = fields.Datetime.now()
        offers = self.search([
            ('status', "not in", ["accepted", "refused"]),
        ])
        for offer in offers:
            expiry_date = offer.create_date + timedelta(days=offer.validity)
            if expiry_date < today:
                offer.write({
                    'status': 'refused'
                })
