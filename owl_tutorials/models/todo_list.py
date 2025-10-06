# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class todo_list(models.Model):
    _name = 'todo.list'
    _description = 'todo list'

    name = fields.Char()
    color = fields.Char()
    completed = fields.Boolean()
