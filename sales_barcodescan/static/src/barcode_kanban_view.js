import { registry } from "@web/core/registry";
import { productCatalogKanbanView } from "@product/product_catalog/kanban_view";
import { BarcodeProductCatalogKanbanModel } from "./barcode_kanban_model";

export const BarcodeProductCatalogKanbanView = {
    ...productCatalogKanbanView,
    Model: BarcodeProductCatalogKanbanModel,
};

registry.category("views").remove("product_kanban_catalog");
registry.category("views").add("product_kanban_catalog", BarcodeProductCatalogKanbanView);
