import { useService } from "@web/core/utils/hooks"
import { registry } from "@web/core/registry"
import { imageField, ImageField } from "@web/views/fields/image/image_field";
import { ImageDialog } from "./image_dialog"

export class ImageClickEnlarge extends ImageField {
    static template = "product_view_kanban_catalog_inherit.image_preview"

    setup() {
        super.setup()
        this.dialog = useService("dialog")
    }

    openImageInDialog(e) {
        if(!this.isMobile){
            return
        }
        e.stopPropagation()
        this.dialog.add(ImageDialog, {
            imgSrc: this.getUrl(this.props.name)
        })
    }
}

export const imageDesigner = {
    ...imageField,
    component: ImageClickEnlarge
}

registry.category("fields").add("custom_image_designer", imageDesigner)
