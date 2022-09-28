/** @odoo-module */

import { Component } from "@odoo/owl";
import { url } from "@web/core/utils/urls";
import { GalleryModel } from "./gallery_model";

export class GalleryImage extends Component {
    static template = "awesome_gallery.GalleryImage";
    static props = {
        record: Object,
        model: GalleryModel,
    };

    get imageUrl() {
        return url("/web/image", {
            model: this.props.model.resModel,
            id: this.props.record.id,
            field: this.props.model.imageField,
        });
    }
}
