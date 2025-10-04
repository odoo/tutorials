import { ProductCatalogKanbanRecord } from "@product/product_catalog/kanban_record";
import { useFileViewer } from "@web/core/file_viewer/file_viewer_hook";


export class ProductCatalogKanbanRecordInherited extends ProductCatalogKanbanRecord {
    setup() {
        super.setup();
        this.fileViewer = useFileViewer();
    }
    onGlobalClick(ev) {
        // Opens pop up dialog box when clicked on product image.
        if (ev.target.closest(".o_product_image_custom")) {
            return;
        }
        super.onGlobalClick(ev)
    }
}
