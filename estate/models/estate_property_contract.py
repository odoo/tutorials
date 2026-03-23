from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyContract(models.Model):
    _name = "estate.property.contract"
    _description = "Property Contract"

    name = fields.Char(
        required=True,
        compute= "_compute_contract_name"
    )

    property_id = fields.Many2one("estate.property", string="Property", required=True)
    buyer_id = fields.Many2one("res.partner", string="Buyer", required=True)
    sign_request_id = fields.Many2one("sign.request", string="Sign Request")
    state = fields.Selection(
        [
            ("new", "New"),
            ("sent", "Contract Sent"),
            ("signed", "Signed"),
            ("done", "Deal Done"),
        ],
        default="new",
    )

    def _compute_contract_name(self):
        for record in self:
            record.name = f"Contract - {record.property_id.name}"

    @api.onchange("property_id")
    def _onchange_property(self):
        for record in self:
            record.buyer_id = record.property_id.buyer_id

    def action_send(self):
        self.ensure_one()

        if not self.buyer_id:
            raise UserError("buyer required")
        if not self.property_id.user_id:
            raise UserError("property must have a salesperson")

        seller = self.property_id.user_id.partner_id

        template = self.env["sign.template"].search(
            [("name", "ilike", "blank")], limit=1
        )
        if not template:
            raise UserError("sign template not found")

        roles = template.sign_item_ids.mapped("responsible_id")
        if len(roles) < 2:
            raise UserError("template must have at least 2 roles")

        buyer_role = roles[0]
        seller_role = roles[1]

        send_request = self.env["sign.send.request"].create(
            {
                "template_id": template.id
            }
        )
        self.env["sign.send.request.signer"].create(
            [
                {
                    "sign_send_request_id": send_request.id,
                    "partner_id": self.buyer_id.id,
                    "role_id": buyer_role.id,
                },
                {
                    "sign_send_request_id": send_request.id,
                    "partner_id": seller.id,
                    "role_id": seller_role.id,
                },
            ]
        )
        sign_request = send_request.create_request()

        if not sign_request:
            raise UserError("failed to create sign request")

        self.sign_request_id = sign_request.id
        self.state = "sent"

    def update_signed_status(self):
        for record in self:
            if record.sign_request_id:
                if record.sign_request_id.state in ("signed", "completed"):
                    record.write({"state": "signed"})

    def action_done(self):
        for record in self:
            if not record.sign_request_id:
                raise UserError("No sign request found.")
            if record.sign_request_id.state not in ("signed", "completed"):
                raise UserError("Contract must be signed first.")
            record.state = "done"
            record.property_id.state = "sold"
