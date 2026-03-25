from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _inherit = "estate.property.offer"

    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        required=True,
        domain="[('id', 'in', allowed_partner_ids)]",
    )

    allowed_partner_ids = fields.Many2many(
        "res.partner", compute="_compute_allowed_partners"
    )

    @api.depends("property_id.event_id.registration_ids")
    def _compute_allowed_partners(self):
        for rec in self:
            abc = rec.property_id.event_id.registration_ids.filtered(
                lambda o: o.state == "done"
            )
            partners = abc.mapped("partner_id")

            for reg in rec.property_id.event_id.registration_ids:
                if not reg.partner_id:
                    partner = self.env["res.partner"].create(
                        {
                            "name": reg.name,
                            "email": reg.email,
                            "phone": reg.phone,
                        }
                    )
                    reg.partner_id = partner
                    partners |= partner

            rec.allowed_partner_ids = partners
