/** @odoo-module **/

import { ProductCatalogKanbanRecord } from "@product/product_catalog/kanban_record";
import { productCatalogKanbanView } from "@product/product_catalog/kanban_view";
import { ProductCatalogKanbanRenderer } from "@product/product_catalog/kanban_renderer";
import { registry } from "@web/core/registry";
import { useFileViewer } from "@web/core/file_viewer/file_viewer_hook";

export class InheritProductMobileCatalog extends ProductCatalogKanbanRecord {
  setup() {
    super.setup();
    this.fileViewer = useFileViewer();
  }

  onGlobalClick(e) {
    const imageContainer = e.target.closest(".o_product_image");
    if (imageContainer) {
      const imageUrl = e.target.getAttribute("src");
      if (imageUrl) {
        this.openImagePreview(imageUrl);
        return;
      }
    }
    super.onGlobalClick(e);
  }

  openImagePreview(imageUrl) {
    const fileModel = {
      isImage: true,
      isViewable: true,
      displayName: imageUrl,
      defaultSource: imageUrl,
      downloadUrl: imageUrl,
    };
    this.fileViewer.open(fileModel);
  }
}

export class InheritProductMobileCatalogRenderer extends ProductCatalogKanbanRenderer {
  static components = {
    ...ProductCatalogKanbanRenderer.components,
    KanbanRecord: InheritProductMobileCatalog,
  };
}

export const ProductMobileKanbanCatalogView = {
  ...productCatalogKanbanView,
  Renderer: InheritProductMobileCatalogRenderer,
};

registry.category("views").add("product_mobile_kanban_catalog", ProductMobileKanbanCatalogView);
