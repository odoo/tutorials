from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):

    _name = 'estate.property.offer'
    _description = "A  model where offer for the properties are stored"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(selection=[('accepted', "Accepted"),
                              ('refused', "Refused")])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one(
        'estate.property', required=True)
    property_type_id = fields.Many2one(
        'estate.property.type', string='property_type_id', related='property_id.property_type_id')
    validity = fields.Integer(string="Validity", default='7')
    date_deadline = fields.Datetime(
        string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for rec in self:
            create_date = rec.create_date or fields.Date.context_today(self)
            rec.date_deadline = fields.Date.add(create_date, days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            create_date = rec.create_date or fields.Date.context_today(self)
            rec.validity = (rec.date_deadline - create_date).days

    def action_status_accepted(self):
        for rec in self:

            if rec.status == 'accepted':
                raise UserError(_("Offer has already been accepted"))
            rec.status = 'accepted'

            rec.property_id.write({
                'buyer_id': rec.partner_id.id,
                'selling_price': rec.price,
                'state': 'offer_accepted'
            })

            (rec.property_id.offer_ids - rec).write({
                'status': 'refused'
            })

        return True

    def action_status_refused(self):
        for rec in self:
            if rec.status == 'refused':
                raise UserError(_("Offer has already been refused"))

            rec.property_id.write({
                'buyer_id': False,
                'selling_price': False,
            })
        return True

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'Offer Price Must Be Greater than zero'
    )

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            property_id = vals.get('property_id')
            if property_id:
                property = self.env['estate.property'].browse(property_id)
                max_existing_offer = property.best_price or 0.0
                price = vals.get('price')
                if price is not None and price < max_existing_offer:
                    raise UserError(_(
                        "The offer must be higher than %(price)s"
                    ) % {'price': max_existing_offer})

                property.state = 'offer_received'
        return super().create(vals_list)
