# fix the ensuing conflict
from odoo import models


class ResUsers(models.Model):
    _inherit = ""

    def do_something(self):
        return True
