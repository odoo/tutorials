/** @odoo-module */

import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";
import { AwesomeKanbanController } from "./kanban_controller";

export const awesomeKanbanView = {
    ...kanbanView,
    Controller: AwesomeKanbanController,
};

registry.category("views").add("awesome_kanban", awesomeKanbanView);
