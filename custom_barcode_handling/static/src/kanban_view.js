import { registry } from "@web/core/registry";
import { productCatalogKanbanView } from "@product/product_catalog/kanban_view";
import { CustomProductCatalogKanbanModel } from "./relational_model";

export const customProductCatalogKanbanView = {
    ...productCatalogKanbanView,
    Model: CustomProductCatalogKanbanModel,
};

registry.category("views").remove("product_kanban_catalog");
registry.category("views").add("product_kanban_catalog", customProductCatalogKanbanView);
