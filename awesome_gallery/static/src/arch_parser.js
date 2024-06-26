/** @odoo-module */

export class GalleryArchParser {
    parse(xmlDoc) {
       const image_field = xmlDoc.getAttribute("image_field");
       const limit = xmlDoc.getAttribute("limit") || 80;;

       return {
            image_field,
            limit
       }
    }
}