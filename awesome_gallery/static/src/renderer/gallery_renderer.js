/** @odoo-module **/
import { Component } from "@odoo/owl";
import { url } from "@web/core/utils/urls";

export class GalleryRenderer extends Component {
    static template = "awesome_dashboard.GalleryRenderer";
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
