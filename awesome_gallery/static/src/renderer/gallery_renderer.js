/** @odoo-module **/
import { Component } from "@odoo/owl";
import { url } from "@web/core/utils/urls";
import { GalleryImage } from "../gallery_image/gallery_image";

export class GalleryRenderer extends Component {
    static template = "awesome_dashboard.GalleryRenderer";
    static components = { GalleryImage };
    static props = {
        state: Object,
    };

    getImageUrl(imageId) {
        return url("/web/image", {
            model: this.props.state.resModel,
            id: imageId,
            field: this.props.state.archInfo.image_field,
        });
    }
}
