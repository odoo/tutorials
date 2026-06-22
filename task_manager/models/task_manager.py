from odoo import api, Command, fields, models
from odoo.exceptions import UserError


class TaskManagerTask(models.Model):
    _name = "task.manager"
    _inherit = ["mail.thread"]
    _description = "Task Manager"

    def _get_default_deadline(self):
        return fields.Datetime.add(fields.Datetime.today(), days=3)

    name = fields.Char(tracking=True, required=True)
    active = fields.Boolean(default=True)
    assigned_user = fields.Many2one("res.users", tracking=True)
    deadline = fields.Datetime(
        tracking=True,
        required=True,
        default=lambda self: self._get_default_deadline(),
    )
    status = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("in_progress", "In Progress"),
            ("done", "Done"),
        ],
        default="new",
        tracking=True,
    )
    tag_ids = fields.Many2many(
        "task.manager.tags",
        compute="_compute_assigned_user",
        store=True,
    )
    days_remaining = fields.Integer(compute="_compute_days_remaining")
    count_of_assignes = fields.Integer(compute="_compute_count_of_assignes")

    @api.depends("deadline")
    def _compute_days_remaining(self):
        for task in self:
            task.days_remaining = (task.deadline - fields.Datetime.today()).days

    @api.depends("assigned_user")
    def _compute_count_of_assignes(self):
        for task in self:
            task.count_of_assignes = len(task.assigned_user)

    @api.depends("assigned_user")
    def _compute_assigned_user(self):
        tag_name = "assigned"
        tag = self.env["task.manager.tags"].search([("name", "=", tag_name)], limit=1)
        if not tag:
            tag = self.env["task.manager.tags"].create({"name": tag_name})

        unlink_ids = []
        link_ids = []

        for task in self:
            if not task.assigned_user and tag in task.tag_ids:
                unlink_ids.append(task.id)
            elif task.assigned_user and tag not in task.tag_ids:
                link_ids.append(task.id)

        if unlink_ids:
            self.browse(unlink_ids).tag_ids = [Command.unlink(tag.id)]
        if link_ids:
            self.browse(link_ids).tag_ids = [Command.link(tag.id)]

    def write(self, vals):
        is_archiving = "active" in vals
        for task in self:
            if task.status == "done" and not is_archiving:
                raise UserError("Cannot update task's details in the Done state.")

        return super().write(vals)

    def quick_archive(self):
        if self:
            tasks = self.filtered(lambda t: t.status == "done" and t.active)
        else:
            tasks = self.env["task.manager"].search(
                [
                    ("status", "=", "done"),
                    ("active", "=", True),
                ],
            )
        if tasks:
            tasks.action_archive()

    def print_task_count(self):
        task_count = self.env["task.manager"].search_count([])
        return {
            "effect": {
                "fadeout": "slow",
                "message": f"{task_count} Tasks are there.",
                "img_url": "/web/static/img/smile.svg",
                "type": "rainbow_man",
            }
        }

    def generate_multiple_tasks(self):
        tasks = [
            {"name": "Generated Task 1", "deadline": fields.Datetime.today()},
            {"name": "Generated Task 2", "deadline": fields.Datetime.today()},
        ]
        self.env["task.manager"].create(tasks)

    def _auto_archive(self):
        done_tasks = self.env["task.manager"].search(
            [
                ("status", "=", "done"),
                ("active", "=", True),
            ],
        )
        done_tasks.action_archive()

    @api.autovacuum
    def _gc_delete_archive_task(self):
        old_archived_tasks = self.env["task.manager"].search(
            [
                ("active", "=", False),
                (
                    "create_date",
                    "<",
                    fields.Datetime.subtract(
                        fields.Datetime.today(),
                        days=31,
                    ),
                ),
            ],
        )
        # breakpoint()
        old_archived_tasks.unlink()
