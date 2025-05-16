import { ImageField, imageField } from "@web/views/fields/image/image_field";
import { useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Dialog } from "@web/core/dialog/dialog";
import { useService } from "@web/core/utils/hooks";


export class ImageDialog extends Dialog {
    static template = "ImageDialog"
    static components = { Dialog }
    
    setup() {
        super.setup()
        this.state = useState({ zoomLevel: 1 })
        this.dialogService = useService("dialog")
    }

    zoomIn() {
        this.state.zoomLevel = Math.min(this.state.zoomLevel + 0.2, 3)
    }

    zoomOut() {
        this.state.zoomLevel = Math.max(this.state.zoomLevel - 0.2, 0.5)
    }
}

export class ZoomableImageField extends ImageField {
    static template = "ZoomableImageField";
    static props = {
        ...ImageField.props,
        zoomType: { type: String, optional: true },
    };
    static defaultProps = {
        ...ImageField.defaultProps,
        zoomType: "click",
    };
    
    setup() {
        super.setup();
        this.dialogService = useService("dialog")
    }

    onClick(ev) {
        if (this.props.zoomType === "click") {
            const imageUrl = ev.target.getAttribute("src")
            this.dialogService.add(ImageDialog, { imageUrl })
        }

    }
}

export const zoomableImageField = {
    ...imageField,
    component: ZoomableImageField,
    supportedOptions: [
        {
            name:"zoom_type",
            type: "string",
            default: "click",
        },
    ],
    supportedTypes: ["binary", "many2one"],
    extractProps: ({ options }) => ({
        zoomType: options.zoom_type,
    }),
};

registry.category("fields").add("zoomable_image", zoomableImageField);
