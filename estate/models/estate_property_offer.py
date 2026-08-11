from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "this model is for estate property offers"
    # _order = "price desc"

    _check_price = models.Constraint(
        "CHECK(price>0)",
        "Price of offer must be positive.",
    )

    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    price = fields.Float()
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")
    property_type_id = fields.Many2one(
        'estate.property.type',
        related="property_id.property_type",
        string="Property Type",
    )
    status = fields.Selection(
        [('accepted', "Accepted"), ('refused', "Refused")],
        copy=False,
    )

    validity = fields.Integer(default=7)

    security_status = fields.Selection(
        [('suspicious', 'Suspicious')],
        compute='_compute_security_status',
    )

    @api.depends("price", "partner_id.name")
    def _compute_display_name(self):
        for offer in self:
            partner_name = offer.partner_id.name if offer.partner_id else ""
            if partner_name:
                offer.display_name = f"${offer.price:,.2f} ({partner_name})"
            else:
                offer.display_name = f"${offer.price:,.2f}"

    @api.depends("create_date", "partner_id")
    def _compute_security_status(self):
        self.security_status = False
        valid_records = self.filtered(
            lambda r: r.id and r.partner_id and r.create_date,
        )
        if not valid_records:
            return

        query = """
                SELECT o1.id
                FROM estate_property_offer o1
                JOIN estate_property_offer o2 ON o1.partner_id = o2.partner_id
                    AND o1.property_id = o2.property_id
                    AND o2.create_date >= o1.create_date - INTERVAL '300 seconds'
                    AND o2.create_date <= o1.create_date + INTERVAL '300 seconds'
                WHERE o1.id IN %s
                GROUP BY o1.id
                HAVING COUNT(o2.id) > 2
                """

        self.env.cr.execute(query, (tuple(valid_records.ids),))
        suspicious_ids = [row[0] for row in self.env.cr.fetchall()]

        if suspicious_ids:
            self.browse(suspicious_ids).write({"security_status": "suspicious"})

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.date_deadline = create_date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() or fields.Date.today()
            if offer.date_deadline and create_date:
                offer.validity = (offer.date_deadline - create_date).days

    def action_accept(self):
        for offer in self:
            property_record = offer.property_id

            already_accepted = property_record.offer_ids.filtered(
                lambda o: (
                    o.price == property_record.selling_price and o.status == 'accepted'
                ),
            )

            if already_accepted:
                already_accepted.status = "refused"

            offer.status = "accepted"
            offer.property_id.write(
                {
                    "selling_price": offer.price,
                    "buyer": offer.partner_id.id,
                    "state": "offer_accepted",
                },
            )
            refuse_ids = property_record.offer_ids.filtered(lambda o: not o.status)
            refuse_ids.write({"status": "refused"})

            existing_active_booking = self.env["estate.property.booking"].search(
                [
                    ("property_id", "=", property_record.id),
                    ("state", "=", "active"),
                ],
                limit=1,
            )
            if not existing_active_booking:
                self.env["estate.property.booking"].create(
                    {
                        "property_id": property_record.id,
                        "state": "active",
                    },
                )
        return True

    def action_make_validity_default(self):
        for offer in self:
            offer.validity = 7
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        props = tuple(
            val.get('property_id') for val in vals_list if val.get('property_id')
        )
        res_group = self.env['estate.property.offer']._read_group(
            domain=[('property_id', 'in', props)],
            groupby=['property_id'],
            aggregates=['price:max'],
        )
        max_offers = {prop.id: max_price for prop, max_price in res_group}

        for val in vals_list:
            prop_id = val.get('property_id')
            price = val.get('price', 0.0)
            max_offer = max_offers.get(prop_id, 0.0)

            if float_compare(price, max_offer, precision_rounding=0.01) <= 0:
                raise UserError(f"The offer must be higher than {max_offer:.2f}")

            max_offers[prop_id] = price

        offers = super().create(vals_list)
        offers.property_id.write({'state': 'offer_received'})
        return offers
