from odoo import models, fields, api


class POSConfigureReceipt(models.TransientModel):
    _name = 'pos.configure.receipt'
    _description = 'POS Configure Receipt'

    pos_config_id = fields.Many2one('pos.config', string="POS Config")
    layout = fields.Selection([
        ('light', 'Light'),
        ('boxed', 'Boxed'),
        ('lined', 'Lined'),
    ], string="Receipt Layout", default='light')

    logo = fields.Binary("Logo")
    header = fields.Html("Header")
    footer = fields.Html("Footer")
    is_restaurant = fields.Boolean(default="true")
    receipt_preview = fields.Html("Receipt Preview", compute="_compute_receipt_preview", store=False)

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
                'is_restaurant': self.is_restaurant
            })

    def action_apply_configuration(self):
        self.ensure_one()
        if self.pos_config_id:
            self.pos_config_id.write({
                'receipt_logo': self.logo,
                'receipt_header': self.header,
                'receipt_footer': self.footer,
                'receipt_layout': self.layout,
            })
        self.env['ir.config_parameter'].sudo().set_param('pos.receipt.layout', self.layout)
        return {'type': 'ir.actions.act_window_close'}
