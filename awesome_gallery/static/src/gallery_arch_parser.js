/** @odoo-module */

export class GalleryArchParser {
    parse(xmlDoc) {
        const imageField = xmlDoc.getAttribute("image_field");
        return {
            imageField,
        };
    }
}
