export class GalleryArchParser {
    parse(xmlDoc) {
        const image_field = xmlDoc.getAttribute("image_field")
        const tooltip_field = xmlDoc.getAttribute("tooltip_field")
        const limit = parseInt(xmlDoc.getAttribute("limit")) || 15;
        return {
            image_field,
            tooltip_field,
            limit,
        }
    }
}