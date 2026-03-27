from odoo import fields, models


class EstatePropertyDeal(models.Model):
    _name = "estate.property.deal"
    _description = "Real Estate Deal"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True, default="deal")
    description = fields.Text()
    date_availability = fields.Date(
        copy=False, default=lambda self: fields.Date.today()
    )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    state = fields.Selection(
        [
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('cancelled', "Cancelled"),
        ],
        copy=False,
        default="new",
    )
    buyer_id = fields.Many2one(
        "res.partner",
        string="Buyer",
        copy=False,
        readonly=True,
    )
    salesperson_id = fields.Many2one(
        "res.users",
        string="Salesperson",
        readonly=True,
    )
    property_id = fields.Many2one("estate.property")

    def action_deal_pdf(self):
        template = self.env.ref("estate_deal.estate_deal_email_template")

        ctx = {
            "default_model": "estate.property.deal",
            "default_res_ids": [self.id],
            "default_template_id": template.id,
            "default_use_template": True,
            "default_partner_ids": [
                self.buyer_id.id,
            ],
        }

        self.property_id.state = "sold"
        self.state = "sold"
        return {
            "name": "Send",
            "type": "ir.actions.act_window",
            "res_model": "mail.compose.message",
            "view_mode": "form",
            "target": "new",
            "context": ctx,
        }

    def action_request_signature(self):
        self.ensure_one()

        template = self.env["sign.template"].search(
            [("name", "=", "Deal Report.pdf")], limit=1
        )

        return {
            "type": "ir.actions.act_window",
            "name": "Request Signature",
            "res_model": "sign.send.request",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_template_id": template.id,
                "default_reference_doc": f"{self._name},{self.id}",
                "default_signer_ids": [
                    (
                        0,
                        0,
                        {
                            "role_id": self.env["sign.item.role"]
                            .search([("name", "=", "Salesperson")], limit=1)
                            .id,
                            "partner_id": self.salesperson_id.partner_id.id,
                        },
                    ),
                    (
                        0,
                        0,
                        {
                            "role_id": self.env["sign.item.role"]
                            .search([("name", "=", "Buyer")], limit=1)
                            .id,
                            "partner_id": self.buyer_id.id,
                        },
                    ),
                ],
            },
        }
