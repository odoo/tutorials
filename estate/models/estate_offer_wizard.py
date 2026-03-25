from odoo import models, fields, api
from odoo.exceptions import UserError


class EstateOfferWizard(models.TransientModel):
    _name = 'estate.offer.wizard'
    _description = 'Create Offer for Multiple Properties'

    partner_id = fields.Many2one(
        'res.partner',
        string="Buyer",
        required=True,
        domain="[('id', 'in', allowed_partner_ids)]"
    )
    price = fields.Float(string="Offer Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    allowed_partner_ids = fields.Many2many(
        'res.partner',
        compute="_compute_allowed_partners"
    )

    @api.depends_context('active_ids')
    def _compute_allowed_partners(self):
        active_ids = self.env.context.get('active_ids', [])
        properties = self.env['estate.property'].browse(active_ids)
        for rec in self:
            partner_sets = []
            for prop in properties:
                p = self.env['res.partner']
                if prop.event_id:
                    p |= prop.event_id.registration_ids.filtered(
                        lambda r: r.state == 'done'
                    ).mapped('partner_id')
                p |= prop.visit_ids.filtered(
                    lambda v: v.state == 'done'
                ).mapped('customer_id')
                partner_sets.append(set(p.ids))
            if partner_sets:
                common_ids = set.intersection(*partner_sets)
            else:
                common_ids = set()
            rec.allowed_partner_ids = [(6, 0, list(common_ids))]

    def action_create_offers(self):
        active_ids = self.env.context.get('active_ids')
        if not active_ids:
            raise UserError("No properties selected.")
        properties = self.env['estate.property'].browse(active_ids)
        errors = []
        for property in properties:
            if property.state in ['sold', 'cancelled']:
                continue
            event_ok = False
            if property.event_id:
                event_ok = property.event_id.registration_ids.filtered(
                    lambda r: r.partner_id.id == self.partner_id.id and r.state == 'done'
                )
            visit_ok = property.visit_ids.filtered(
                lambda v: v.customer_id.id == self.partner_id.id and v.state == 'done'
            )
            if not (event_ok or visit_ok):
                errors.append(f"{property.name}: Customer did not attend event or visit")
                continue
            self.env['estate.property.offer'].create({
                'property_id': property.id,
                'partner_id': self.partner_id.id,
                'price': self.price,
                'validity': self.validity,
            })
        if errors:
            raise UserError("\n".join(errors))
