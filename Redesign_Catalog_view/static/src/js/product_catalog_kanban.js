import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";
import { ProductCatalogKanbanRecord } from "@product/product_catalog/kanban_record";
import { ProductCatalogKanbanRenderer } from "@product/product_catalog/kanban_renderer";
import { productCatalogKanbanView } from "@product/product_catalog/kanban_view";

class ImageDialog extends Component {
    static components = { Dialog };
    static template = "product_catalog_redesign.ImageDialog";
    static props = ["imageUrl", "close"];
}

class ProductCatalogKanbanRecordInherited extends ProductCatalogKanbanRecord {
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    }

    onGlobalClick(ev) {
        const imageElement = ev.target.closest(".o_product_image_custom img");
        if (imageElement) {
            this.dialogService.add(ImageDialog, {
                imageUrl: imageElement.src,
                close: () => this.dialogService.close(),
            });
            return;
        }

        if (ev.target.closest(".o_product_catalog_cancel_global_click")) {
            return;
        }

        this.productCatalogData.quantity === 0 ? this.addProduct() : this.increaseQuantity();
    }
}

class InheritProductCatalogKanbanRenderer extends ProductCatalogKanbanRenderer {
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
