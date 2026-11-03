{
    "name": "Task Manager",
    "application": True,
    "installable": True,
    "author": "sngoh",
    "depends": ["mail"],
    "license": "LGPL-3",
    "data": [
        "security/ir.access.csv",
        "data/ir_cron_data.xml",
        "views/task_manager_tags_view.xml",
        "views/task_manager_view.xml",
        "views/task_manager_menus.xml",
    ],
    "pre_init_hook": "_pre_init_hook",
    "post_init_hook": "add_tags",
    "uninstall_hook": "remove_users_with_mobile_number",
}
