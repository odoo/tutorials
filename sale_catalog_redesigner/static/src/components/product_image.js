import { useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { imageField, ImageField } from "@web/views/fields/image/image_field";
import { ImageDialog } from "./product_image_dialog";

export class ImageClickEnlarge extends ImageField {
    static template = "product_view_kanban_catalog_inherit.image_preview";

    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this.ui = useService("ui");
    }

    openImageInDialog(e) {
        if (!this.ui.isSmall) {
            return;
        }
        e.stopPropagation();

        const record = this.props.record;
        if (!record || !record.resId) return;

        const resId = record.resId;
        const resModel = record.resModel || "product.product";
        const cleanImgSrc = `${window.location.origin}/web/image?model=${resModel}&id=${resId}&field=image_1920`;
        const productName = record.data.display_name || record.data.name || "Product";

        this.dialog.add(ImageDialog, {
            imgSrc: cleanImgSrc,
            productName: productName,
        });
    }
}

export const imageDesigner = {
    ...imageField,
    component: ImageClickEnlarge
};

registry.category("fields").add("custom_image_designer", imageDesigner);
