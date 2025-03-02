import { productCatalogKanbanView } from "@product/product_catalog/kanban_view";
import { registry } from "@web/core/registry";
import { ProductCatalogPopupKanbanRenderer } from "./kanban_renderer";

export const productCatalogPopupKanbanView = {
    ...productCatalogKanbanView,
    Renderer: ProductCatalogPopupKanbanRenderer,
};

registry.category("views").add("product_popoup_kanban_catalog", productCatalogPopupKanbanView);
