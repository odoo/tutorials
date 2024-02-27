/** @odoo-module */

import { Component } from "@odoo/owl";
import { url } from "@web/core/utils/urls";
import { GalleryModel } from "./gallery_model";
import { useService } from "@web/core/utils/hooks";
import { FileUploader } from "@web/views/fields/file_handler";
import { useTooltip } from "@web/core/tooltip/tooltip_hook";

export class GalleryImage extends Component {
    static template = "awesome_gallery.GalleryImage";
    static components = { FileUploader };
    static props = {
        record: Object,
        model: GalleryModel,
        onImageUpload: Function,
        tooltipTemplate: {
            optional: true,
            type: String
        }
    };

    setup() {
        this.actionService = useService("action");

        if(this.props.tooltipTemplate) {
            useTooltip("tooltip", {
                info: { record: this.props.record },
                template: this.props.tooltipTemplate,
            });
        }
    }

    onClickImage(id) {
        this.actionService.switchView("form", {resId: id});
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
