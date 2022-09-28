import { Component } from "@odoo/owl";
import { GalleryModel } from "./gallery_model";
import { GalleryImage } from "./gallery_image";

export class GalleryRenderer extends Component {
    static components = { GalleryImage };
    static template = "awesome_gallery.GalleryRenderer";
    static props = {
        model: GalleryModel,
    }
}
