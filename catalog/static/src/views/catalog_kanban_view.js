/** @odoo-module **/

import { kanbanView } from "@web/views/kanban/kanban_view";
import { registry } from "@web/core/registry";

import { CatalogKanbanController } from "./catalog_kanban_controller";
import { CatalogKanbanRenderer } from "./catalog_kanban_renderer";
import { ProductCatalogSearchPanel} from "@product/product_catalog/search/search_panel";

export const CatalogKanbanView = {
    ...kanbanView,
    Controller: CatalogKanbanController,
    Renderer: CatalogKanbanRenderer,
    SearchPanel: ProductCatalogSearchPanel
};

registry.category("views").add('kanban_catalog', CatalogKanbanView);
