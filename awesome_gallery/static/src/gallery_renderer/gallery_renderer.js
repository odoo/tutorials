import { url } from "@web/core/utils/urls";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

import { GalleryModel } from "../gallery_model";


export class GalleryRenderer extends Component {
    static template = "awesome_gallery.GalleryRenderer";
    static props = { model: GalleryModel };

    setup() {
        this.action_service = useService("action");
    }

    getImageUrl(record_id) {
        return url("/web/image", {
            model: this.props.model.resModel,
            id: record_id,
            field: this.props.model.imageField,
        });
    }

    openFormView(record_id) {
        this.action_service.switchView("form", { resId: record_id });
    }
}
