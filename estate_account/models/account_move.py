from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    property_ids = fields.One2many(
        'estate.property', 'invoice_id',
        string='Properties', readonly=True, copy=False)
    property_count = fields.Integer(compute="_compute_property_count", string='Property Count')

    @api.depends('property_ids')
    def _compute_property_count(self):
        for move in self:
            move.property_count = len(move.property_ids)

    def action_view_properties(self):
        self.ensure_one()

        source_properties = self.property_ids
        result = self.env['ir.actions.act_window']._for_xml_id('estate.estate_property_action')
        if len(source_properties) > 1:
            result['domain'] = [('id', 'in', source_properties.ids)]
        elif len(source_properties) == 1:
            result['views'] = [(self.env.ref('estate.estate_property_view_form', False).id, 'form')]
            result['res_id'] = source_properties.id
        else:
            result = {'type': 'ir.actions.act_window_close'}
        return result
