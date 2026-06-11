import { registry } from "@web/core/registry";
import { kanbanView } from "@web/views/kanban/kanban_view";

export const awesomeKanbanView = {
    ...kanbanView,
};

registry.category("views").add("awesome_kanban", awesomeKanbanView);
