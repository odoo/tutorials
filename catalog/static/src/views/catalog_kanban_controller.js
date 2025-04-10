/** @odoo-module **/

import { useService } from "@web/core/utils/hooks";
import { KanbanController } from "@web/views/kanban/kanban_controller";

export class CatalogKanbanController extends KanbanController {
    static template = "CatalogKanbanController";

    setup() {
        super.setup();
        this.action = useService("action");
    }

    async goBack() {
        try {
            if (this.action.restore && this.env.config.breadcrumbs.length > 1) {
                await this.action.restore();
            } else {
                await this.action.doAction({ type: "ir.actions.act_window_close" });
            }
        } catch (error) {
            console.error("Error in goBack:", error);
        }
    }
}
