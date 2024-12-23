from odoo import models, fields


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_change_state(self):
        param_value = self.env.context.get("param_name", "default_value")

        if param_value == "sold":

            self.state = "sold"
            whatsapp_composer = (
                self.env["whatsapp.composer"]
                .with_context({"active_id": self.id})
                .create(
                    {
                        "wa_template_id": self.env.company.wa_sale_template_id.id,
                        "res_model": "estate.property",
                    }
                )
            )
            whatsapp_composer.sudo()._send_whatsapp_template(force_send_by_cron=True)

        else:
            return super().action_change_state()
