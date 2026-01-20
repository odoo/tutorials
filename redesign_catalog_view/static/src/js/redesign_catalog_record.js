import { ProductCatalogKanbanRecord } from "@product/product_catalog/kanban_record";
import { useFileViewer } from "@web/core/file_viewer/file_viewer_hook";

export class RedesignCatalogViewRecord extends ProductCatalogKanbanRecord {
  setup() {
    super.setup();
    this.fileViewer = useFileViewer();
  }

  onGlobalClick(e) {
    const imageContainer = e.target.closest(".o_product_image");
    if (imageContainer) {
      const imageUrl = e.target.getAttribute("src");

      if (imageUrl) {
        this.openImage(imageUrl);
        return;
      }
    }
    super.onGlobalClick(e);
  }

  openImage(imageUrl) {
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
