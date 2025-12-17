import { registry } from "@web/core/registry";
import { productCatalogKanbanView } from "@product/product_catalog/kanban_view";
import { SortProductCatalogKanbanModel } from "./kanban_model";

export const SortedProductCatalogKanbanView = {
    ...productCatalogKanbanView,
    Model: SortProductCatalogKanbanModel,
};

registry.category("views").remove("product_kanban_catalog");
registry.category("views").add("product_kanban_catalog", SortedProductCatalogKanbanView);
