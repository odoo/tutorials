import { productCatalogKanbanView } from "@product/product_catalog/kanban_view";
import { registry } from "@web/core/registry";
import { RedesignCatalogViewRenderer } from "./redesign_catalog_renderer";

export const RedesignCatalogView = {
  ...productCatalogKanbanView,
  Renderer: RedesignCatalogViewRenderer,
};

registry
  .category("views")
  .add("product_mobile_kanban_catalog", RedesignCatalogView);
