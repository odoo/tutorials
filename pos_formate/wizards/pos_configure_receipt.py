from odoo import models, fields, api
from odoo.tools import html2plaintext


class POSConfigureReceipt(models.TransientModel):
    _name = 'pos.configure.receipt'
    _description = 'POS Configure Receipt'

    pos_config_id = fields.Many2one(
        'pos.config',
        string="POS Config",
        default=lambda self: self.env.context.get('default_pos_config_id'),
        required=True
    )
    layout = fields.Selection([
        ('light', 'Light'),
        ('boxed', 'Boxed'),
        ('lined', 'Lined'),
    ], string="Receipt Layout", default='light')

    logo = fields.Binary("Logo")
    header = fields.Html("Header")
    footer = fields.Html("Footer")
    receipt_preview = fields.Html("Receipt Preview", compute="_compute_receipt_preview", store=False)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        pos_config_id = self.env.context.get('default_pos_config_id')
        if pos_config_id:
            pos_config = self.env['pos.config'].browse(pos_config_id)
            res.update({
                'layout': pos_config.receipt_layout or 'light',
                'logo': pos_config.receipt_logo,
                'header': pos_config.receipt_header,
                'footer': pos_config.receipt_footer,
            })
        return res

    @api.depends('layout', 'logo', 'header', 'footer')
    def _compute_receipt_preview(self):
        for record in self:
            template_id = {
                'light': 'pos_formate.custom_receipt_light',
                'boxed': 'pos_formate.custom_receipt_boxes',
                'lined': 'pos_formate.custom_receipt_lined',
            }.get(record.layout, 'pos_formate.custom_receipt_light')

            record.receipt_preview = self.env['ir.ui.view']._render_template(template_id, {
                'logo': record.logo,
                'header': record.header or '',
                'footer': record.footer or '',
                'company_name': self.env.company.name,
                'company_address': self.env.company.partner_id.contact_address or '',
                'tax_id': self.env.company.vat or '',
                'order_number': "0001-003-0004",
                'date': fields.Datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                'orderlines': [
                    {"no": 1, "name": "Margarita Pizza", "qty": 3, "price": 200, "hsn": "2300976"},
                    {"no": 2, "name": "Bacon Burger", "qty": 5, "price": 150, "hsn": ""},
                    {"no": 3, "name": "Apple Pie", "qty": 3, "price": 80, "hsn": "2300976"},
                ],
                'taxes': [
                    {"name": "SGST 2.5%", "amount": 40.2, "base": 1584.8, "total": 1625},
                    {"name": "CGST 2.5%", "amount": 40.2, "base": 1584.8, "total": 1625},
                ],
                'total_qty': 12,
                'sub_total': 1625,
                'payment_method': "Cash",
                'paid_amount': 1625,
            })

    def action_apply_configuration(self):
        self.ensure_one()
        if self.pos_config_id:
            header = html2plaintext(self.header or "").strip()
            footer = html2plaintext(self.footer or "").strip()

            self.pos_config_id.write({
                'receipt_logo': self.logo,
                'receipt_header': header,
                'receipt_footer': footer,
                'receipt_layout': self.layout,
            })
        self.env['ir.config_parameter'].sudo().set_param('pos.receipt.layout', self.layout)
        return {'type': 'ir.actions.act_window_close'}
