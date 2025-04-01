import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { ImageField } from "@web/views/fields/image/image_field";
import { Component } from "@odoo/owl";

export class FullScreenImage extends Component {
    static template = "product_kanban_inherit.PopUp";
    static props = {
        src: { type: String },
        close: Function,
    };
}

export class ImagePreviewField extends ImageField {
    static template = "product_kanban_inherit.ShowImage";

    setup() {
        super.setup();
        this.dialog = useService("dialog");
    }

    openImageFullScreen() {
        if (this.env.isSmall) {
            this.dialog.add(FullScreenImage, {
                src: this.getUrl(this.props.name),
            });
        }
    }
}

export const imageClickEnlarge = {
    component: ImagePreviewField,
};

registry.category("fields").add("image_preview_1", imageClickEnlarge);
