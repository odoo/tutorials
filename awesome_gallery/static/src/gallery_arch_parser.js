/** @odoo-module **/

import { GraphArchParser } from "@web/views/graph/graph_arch_parser";

export class GalleryXmlArchParser extends GraphArchParser {
    parse(xmlDoc) {
        return {
            image_field: xmlDoc.getAttribute("image_field"),
            tooltip_field: xmlDoc.getAttribute("tooltip_field"),
        };
    }
}
