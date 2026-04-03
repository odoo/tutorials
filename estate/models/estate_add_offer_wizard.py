from odoo import fields, models, api
from odoo.exceptions import UserError


class EstateAddOfferWizard(models.TransientModel):
    _name = "estate.add.offer.wizard"
    _description = "Add Offer Wizard"

    price = fields.Float(string="Price", required=True)

    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        required=True,
        domain="[('id', 'in', allowed_partner_ids)]"
    )

    validity = fields.Integer(string="Validity (days)", default=7)

    allowed_partner_ids = fields.Many2many(
        "res.partner",
        compute="_compute_allowed_partner_ids"
    )

    @api.depends_context('active_ids')
    def _compute_allowed_partner_ids(self):
        active_ids = self.env.context.get('active_ids', [])
        properties = self.env['estate.property'].browse(active_ids)

        for rec in self:
            partner_sets = []

            for prop in properties:
                partners = self.env['res.partner']
                if prop.event_id:
                    partners |= prop.event_id.registration_ids.filtered(
                        lambda r: r.state == 'done'
                    ).mapped('partner_id')

                partners |= prop.visit_ids.filtered(
                    lambda v: v.state == 'done'
                ).mapped('customer_id')

                partner_sets.append(set(partners.ids))

            if partner_sets:
                all_ids = set.union(*partner_sets)
            else:
                all_ids = set()

            rec.allowed_partner_ids = [(6, 0, list(all_ids))]

    def action_add_offer(self):
        active_ids = self.env.context.get('active_ids', [])

        if not active_ids:
            raise UserError("No properties selected.")

        properties = self.env["estate.property"].browse(active_ids)

        created_count = 0
        skipped_count = 0
        errors = []

        for prop in properties:

            if prop.state in ["offer_accepted", "sold", "cancelled"]:
                skipped_count += 1
                continue

            event_ok = False
            if prop.event_id:
                event_ok = prop.event_id.registration_ids.filtered(
                    lambda r: r.partner_id.id == self.partner_id.id and r.state == 'done'
                )

            visit_ok = prop.visit_ids.filtered(
                lambda v: v.customer_id.id == self.partner_id.id and v.state == 'done'
            )

            if not (event_ok or visit_ok):
                errors.append(f"{prop.name}: Customer did not attend event or visit")
                continue

            self.env["estate.property.offer"].create({
                "property_id": prop.id,
                "partner_id": self.partner_id.id,
                "price": self.price,
                "validity": self.validity,
            })

            created_count += 1

        if errors:
            raise UserError("\n".join(errors))

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Bulk Offer Result',
                'message': f"{created_count} offers created, {skipped_count} skipped.",
                'type': 'success' if created_count else 'warning',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
