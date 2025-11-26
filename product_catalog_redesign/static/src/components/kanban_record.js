import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Dialog } from "@web/core/dialog/dialog";
import { ProductCatalogKanbanRecord } from "@product/product_catalog/kanban_record";

export class ProductCatalogKanbanRecordInherited extends ProductCatalogKanbanRecord {
    setup() {
        super.setup();
        this.dialogService = useService("dialog");
    }
    
    onGlobalClick(ev) {
        // Opens pop-up dialog box when clicking on a product image.
        if (ev.target.closest(".o_product_image_custom")) {
            const imageUrl = ev.target.getAttribute("src");
            this.showImagePopup(imageUrl);
            return;
        }
        if (ev.target.closest(".o_product_catalog_cancel_global_click")) {
            return;
        }
        if (this.productCatalogData.quantity === 0) {
            this.addProduct();
        } else {
            this.increaseQuantity();
        }
    }

    showImagePopup(imageUrl) {
        this.dialogService.add(ImageDialog, {
            imageUrl: imageUrl,
            close: () => this.dialogService.close(),
        });
    }
}

export class ImageDialog extends Component {
    static components = { Dialog };
    static template = "product_catalog_redesign.ImageDialog";
    static props = ["imageUrl", "close"];

    setup() {
        this.state = useState({
            imageUrl: this.props.imageUrl,
        });
    }
}
