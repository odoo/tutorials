import { useService } from "@web/core/utils/hooks";
import { url } from "@web/core/utils/urls";
import { Component } from "@odoo/owl";
import { FileUploader } from "@web/views/fields/file_handler";

import { GalleryModel } from "../gallery_model";


export class GalleryRenderer extends Component {
    static template = "awesome_gallery.GalleryRenderer";
    static props = { model: GalleryModel };
    static components = { FileUploader };

    setup() {
        this.action_service = useService("action");
        this.orm = useService("orm");
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

    async onFileUploaded(record_id, { data }) {
        await this.orm.webSave(
            this.props.model.resModel,
            [record_id],
            {
                [this.props.model.imageField]: data,
            },
            {
                specification: {},
            }
        )
        await this.props.model.load([]);
    }
}
