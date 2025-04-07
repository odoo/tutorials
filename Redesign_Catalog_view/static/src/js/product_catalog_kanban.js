import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { ProductCatalogKanbanRecord } from "@product/product_catalog/kanban_record";
import { ProductCatalogKanbanRenderer } from "@product/product_catalog/kanban_renderer";
import { productCatalogKanbanView } from "@product/product_catalog/kanban_view";

class ImageDialog extends Component {
    static template = "product_catalog_redesign.ImageDialog";
    static props = ["imageUrl"];

    setup() {
        this.state = useState({ zoom: 1 });
        this.updateZoom = this.updateZoom.bind(this);
    }

    updateZoom(value) {
        this.state.zoom = Math.max(0.5, Math.min(3, this.state.zoom + value));
    }
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
            });
           
            return;
        }

        if (ev.target.closest(".o_product_catalog_cancel_global_click")) {
            console.log("hiii");
            return;
        }
        if (this.productCatalogData.quantity === 0) {
            this.addProduct();
        } else {
            this.increaseQuantity();
        }

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
