from odoo import models, fields
from odoo.exceptions import UserError


class EstateContract(models.Model):
    _name = 'estate.contract'
    _description = 'Property Contract'

    property_id = fields.Many2one('estate.property', required=True)
    buyer_id = fields.Many2one('res.partner', required=True)
    seller_id = fields.Many2one('res.partner', required=True)
    offer_id = fields.Many2one('estate.property.offer', string="Offer", required=True)
    offer_price = fields.Float(related='offer_id.price', string="Offer Price", store=True)
    sign_request_id = fields.Many2one('sign.request')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent for Signature'),
        ('signed', 'Signed'),
        ('done', 'Done'),
    ], default='draft')

    def action_send_for_signature(self):
        template = self.env['sign.template'].search([], limit=1)
        if not template:
            raise UserError("No Sign Template found!")
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
                'partner_id': self.seller_id.id,
                'sign_send_request_id': send_request.id,
                'role_id': template.sign_item_ids[1].responsible_id.id,
            }
        ]
        self.env['sign.send.request.signer'].create(signer_data)
        sign_request = send_request.create_request()
        if sign_request:
            self.sign_request_id = sign_request.id
            self.state = 'sent'

    def action_check_signed(self):
        if self.sign_request_id.state == 'signed':
            self.state = 'signed'
