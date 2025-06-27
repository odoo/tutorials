import json
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    statistics = fields.Json()

    def set_statistics(self, statistics):
        for user in self:
            user.statistics = json.dumps(statistics)
        return True
