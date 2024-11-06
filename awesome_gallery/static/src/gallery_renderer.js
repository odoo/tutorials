/** @odoo-module */

const {Component} = owl;
import {GalleryImage} from "./gallery_image/gallery_image";
import {useService} from "@web/core/utils/hooks";

export class GalleryRenderer extends Component {
    static template = "awesome_gallery.Renderer";
    static props = {
        images: Array,
        imageField: String,
        tooltipField: String,
    }
    static components = {GalleryImage};

    setup(){
        this.actionService = useService("action");
    }

    onImageClick(imageId) {
        this.actionService.switchView("form", {imageId});
    }
}
