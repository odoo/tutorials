from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ResPartnerConvertWizard(models.TransientModel):
    _name = "res.partner.convert.wizard"
    _description = "Convert Partner Wizard"

    partner_id = fields.Many2one("res.partner", required=True, readonly=True)
    to_is_company = fields.Boolean(string="Convert to Company", default=False)

    warning_html = fields.Html(compute="_compute_warning_html", sanitize=False, readonly=True)

    @api.depends("partner_id", "to_is_company")
    def _compute_warning_html(self):
        for w in self:
            if not w.partner_id:
                w.warning_html = ""
                continue

            if w.to_is_company:
                w.warning_html = _(
                    "<p>This will convert the contact to a <b>Company</b>.</p>"
                )
            else:
                w.warning_html = _(
                    "<p>You are converting this <b>Company</b> contact to an <b>Personal</b>.</p>"
                    "<p>The following company-only fields will be cleared:</p>"
                    "<ul>"
                    "<li><b>Capacity (tons)</b></li>"
                    "<li><b>Product Categories</b></li>"
                    "<li><b>Company Status</b></li>"
                    "</ul>"

                )

    def action_confirm(self):
        self.ensure_one()
        partner = self.partner_id
        if not partner:
            raise UserError(_("No contact selected."))

        if self.to_is_company:
            partner.write({"is_company": True})
            return {"type": "ir.actions.act_window_close"}

        if not partner.is_company:
            raise UserError(_("This contact is already an Individual."))

        # clear first, then convert (single write, safe order)
        partner.with_context(allow_company_to_person=True).write({
            "capacity_tons": 0.0,
            "partner_status_id": False,
            "product_category_ids": [(5, 0, 0)],
            "is_company": False,
        })

        return {"type": "ir.actions.act_window_close"}
