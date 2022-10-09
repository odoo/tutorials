import { kanbanView } from "@web/views/kanban/kanban_view";
import { registry } from "@web/core/registry";
import { useInterval } from "../utils/useInterval";

class ShelterKanbanController extends kanbanView.Controller {

    setup() {
        super.setup();
        useInterval(this.reload.bind(this), 10000);
    }

    reload() {
        this.model.load();
    }

}

const shelterKanbanView = {
    ...kanbanView,
    Controller: ShelterKanbanController,
};

registry.category("views").add("shelter_kanban", shelterKanbanView);
