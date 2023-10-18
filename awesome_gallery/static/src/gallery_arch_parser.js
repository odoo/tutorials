/** @odoo-module */

import { visitXML } from "@web/core/utils/xml";

export class GalleryArchParser {
    parse(xmlDoc) {
        const imageField = xmlDoc.getAttribute("image_field");
        const limit = xmlDoc.getAttribute("limit") || 80;
        const fieldsForTooltip = [];
        let tooltipTemplate = undefined;
        visitXML(xmlDoc, (node) => {
            if (node.tagName === "field") {
                fieldsForTooltip.push(node.getAttribute("name"));
            }
            if (node.tagName === "tooltip-template") {
                tooltipTemplate = node;
            }
        })
        return {
            imageField,
            limit,
            fieldsForTooltip,
            tooltipTemplate,
        };
    }
}
