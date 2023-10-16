/** @odoo-module */

import { Component } from "@odoo/owl";
import { url } from "@web/core/utils/urls";
import { GalleryModel } from "./gallery_model";
import { useService } from "@web/core/utils/hooks";
import { FileUploader } from "@web/views/fields/file_handler";

export class GalleryImage extends Component {
    static components = { FileUploader }
    static template = "awesome_gallery.GalleryImage";
    static props = {
        record: Object,
        model: GalleryModel,
        onImageUpload: Function,
    };

    setup() {
        this.action = useService("action");
    }

    onImageClick(resId) {
        this.action.switchView("form", { resId });
    }

    get imageUrl() {
        return url("/web/image", {
            model: this.props.model.resModel,
            id: this.props.record.id,
            field: this.props.model.imageField,
            unique: this.props.record.write_date,
        });
    }

    async _onFileUploaded({ data }) {
        await this.props.onImageUpload(this.props.record.id, data);
    }
}
