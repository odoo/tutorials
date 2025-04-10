/** @odoo-module **/

import { KanbanRenderer } from "@web/views/kanban/kanban_renderer";
import { CatalogKanbanRecord } from './catalog_kanban_record'

export class CatalogKanbanRenderer extends KanbanRenderer {
    static components = {
        ...KanbanRenderer.components,
        KanbanRecord: CatalogKanbanRecord,
    };
}
