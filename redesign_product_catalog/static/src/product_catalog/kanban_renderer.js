import { ProductCatalogKanbanRenderer } from "@product/product_catalog/kanban_renderer";
import { ProductCatalogPopupKanbanRecord } from "./kanban_record";

export class ProductCatalogPopupKanbanRenderer extends ProductCatalogKanbanRenderer {
    static components = {
        ...ProductCatalogKanbanRenderer.components,
        KanbanRecord: ProductCatalogPopupKanbanRecord,
    };
}
