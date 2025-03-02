import { ProductCatalogKanbanRecord } from "@product/product_catalog/kanban_record";

export class ProductCatalogPopupKanbanRecord extends ProductCatalogKanbanRecord {
    onGlobalClick(ev) {
        if (ev.target.closest(".o_product_catalog_cancel_global_click")) {
            return;
        }

        // New condition: Prevent the product from being added if clicked on image in mobile
        if (this.env.isSmall && ev.target.closest(".o_product_image")) {
            return;
        }

        super.onGlobalClick(ev);
    }
}
