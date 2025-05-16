import { registry } from "@web/core/registry";
import { ProductCatalogKanbanRecordInherited } from "./kanban_record";
import { productCatalogKanbanView } from "@product/product_catalog/kanban_view";
import { ProductCatalogKanbanRenderer } from "@product/product_catalog/kanban_renderer";

export class InheritProductCatalogKanbanRenderer extends ProductCatalogKanbanRenderer {
    static components = {
        ...ProductCatalogKanbanRenderer.components,
        KanbanRecord: ProductCatalogKanbanRecordInherited,
    };
}

export const InheritProductCatalogKanbanView = {
    ...productCatalogKanbanView,
    Renderer: InheritProductCatalogKanbanRenderer,
};

registry.category("views").add("product_kanban_catalog_inherit", InheritProductCatalogKanbanView);
