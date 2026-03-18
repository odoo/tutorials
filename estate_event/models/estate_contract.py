from odoo import api, models, fields
from odoo.exceptions import UserError

class EstateContract(models.Model):
    _name = 'estate.contract'
    _description = 'Estate Contract'

    name = fields.Char(default="New Contract", tracking=True)

    property_id = fields.Many2one('estate.property', readonly=True)
    offer_id = fields.Many2one('estate.property.offer')

    buyer_id = fields.Many2one('res.partner', readonly=True)
    salesperson_id = fields.Many2one('res.users', required=True)
    price = fields.Float(string="Price", readonly=True)

    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('signed', 'Signed')
    ], default='scheduled', tracking=True)

    sign_request_id = fields.Many2one('sign.request')

    def action_send_for_sign(self):
        self.ensure_one()

        template = self.env['sign.template'].search([], limit=1)
        if not template:
            raise ValueError("No Sign Template found!")

        send_request = self.env['sign.send.request'].create({
            'template_id': template.id,
            'subject': f"Signature Request for {self.property_id.name}",
            'filename': f"{self.property_id.name}.pdf",
        })

        signer_data = [
            {
                'partner_id': self.buyer_id.id,
                'sign_send_request_id': send_request.id,
                'role_id': template.sign_item_ids[0].responsible_id.id,
            },
            {
                'partner_id': self.salesperson_id.partner_id.id,
                'sign_send_request_id': send_request.id,
                'role_id': template.sign_item_ids[1].responsible_id.id,
            }
        ]
        self.env['sign.send.request.signer'].create(signer_data)

        sign_request = send_request.create_request()

        if sign_request:
            self.sign_request_id = sign_request.id
            self.state = 'in_progress'

            send_request.send_request()

            return {
                'name': 'Sign Contract',
                'type': 'ir.actions.act_window',
                'res_model': 'sign.request',
                'view_mode': 'form',
                'res_id': sign_request.id,
                'target': 'current',
            }

class SignRequest(models.Model):
    _inherit = 'sign.request'

    def write(self, vals):
        res = super().write(vals)

        if 'state' in vals and vals['state'] in ['signed', 'done']:
            contracts = self.env['estate.contract'].search([
                ('sign_request_id', 'in', self.ids)
            ])
            for contract in contracts:
                contract.state = 'signed'
                if contract.property_id:
                    contract.property_id.state = 'sold'

        return res  