import { ImageField } from "@web/views/fields/image/image_field";
import { registry } from "@web/core/registry";
import { useFileViewer } from "@web/core/file_viewer/file_viewer_hook";

export class ImagePreviewField extends ImageField{

    static template = "redesign_catalog_view.ShowImage";

    setup(){
        super.setup();
        this.fileViwer = useFileViewer();
    }

    openImage(event){
        event.stopPropagation();
        event.preventDefault();
            const img_url= this.getUrl(this.props.name);
            if(img_url){
                this.fileViwer.open({
                    isImage: true,
                    isViewable: true,
                    defaultSource: img_url,
                    downloadUrl: img_url,
                })
            }
    }
}

registry.category("fields").add("image_custom", {
    component: ImagePreviewField,
})
