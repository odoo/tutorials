/** @odoo-module */

export class GalleryArchParser {

    parse(xmlDoc) {
        const imageField = xmlDoc.getAttribute("image_field");
        const limit = xmlDoc.getAttribute("limit") || 80;
        return {
            imageField,
            limit,
        };
    }

}
