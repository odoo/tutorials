# -*- coding: utf-8 -*-

from odoo import models, fields, api


class todo_list(models.Model):
    _name = 'todo.list'
    _description = 'todo list'

    name = fields.Char()
    color = fields.Char()
    completed = fields.Boolean()