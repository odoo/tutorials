import { ImageField } from "@web/views/fields/image/image_field";
import { registry } from "@web/core/registry";
import { useFileViewer } from "@web/core/file_viewer/file_viewer_hook";

export class ImagePreviewField extends ImageField {
    static template = "product_kanban_catalog_inherit.ShowImage";
    setup() {
        super.setup();
        this.fileViewer = useFileViewer();
    }

    openImageFullScreen(event) {
        event.stopPropagation();
        event.preventDefault();
        if (this.env.isSmall) {
            const imageUrl = this.getUrl(this.props.name);  // Get the image URL
            if (imageUrl) {
                this.fileViewer.open({
                    isImage: true,
                    isViewable: true,
                    defaultSource: imageUrl,
                    downloadUrl: imageUrl,
                });
            }
        }
    }
}

registry.category("fields").add("image_custom", { component: ImagePreviewField, });
