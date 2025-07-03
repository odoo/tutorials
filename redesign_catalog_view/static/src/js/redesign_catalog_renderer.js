import { ProductCatalogKanbanRenderer } from "@product/product_catalog/kanban_renderer";
import { RedesignCatalogViewRecord } from "./redesign_catalog_record";
export class RedesignCatalogViewRenderer extends ProductCatalogKanbanRenderer {
  static components = {
    ...ProductCatalogKanbanRenderer.components,
    KanbanRecord: RedesignCatalogViewRecord,
  };
}
