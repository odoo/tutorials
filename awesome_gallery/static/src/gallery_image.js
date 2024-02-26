/** @odoo-module */

import { Component } from "@odoo/owl";
import { url } from "@web/core/utils/urls";
import { GalleryModel } from "./gallery_model";
import { useService } from "@web/core/utils/hooks";

export class GalleryImage extends Component {
    static template = "awesome_gallery.GalleryImage";
    static props = {
        record: Object,
        model: GalleryModel,
    };

    setup() {
        this.actionService = useService("action");
    }

    onClickImage(id) {
        this.actionService.switchView("form", {resId: id});
    }

    get imageUrl() {
        return url("/web/image", {
            model: this.props.model.resModel,
            id: this.props.record.id,
            field: this.props.model.imageField,
        });
    }
}
