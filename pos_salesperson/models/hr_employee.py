# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.model
    def _load_pos_data_domain(self, data):
        return []

    @api.model
    def _load_pos_data_fields(self, config_id):
        return ['id', 'name', 'job_title', 'image_1920']

    @api.model
    def _load_pos_data(self, data):
        domain = self._load_pos_data_domain(data)
        fields = self._load_pos_data_fields(data['pos.config']['data'][0]['id'])
        user = self.search_read(domain, fields, order="name")
        return {
            'data': user,
            'fields': fields,
        }
