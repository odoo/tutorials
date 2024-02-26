/** @odoo-module */

import { Component } from "@odoo/owl";
import { GalleryModel } from "./gallery_model";
import { GalleryImage } from "./gallery_image";

export class GalleryRenderer extends Component {
    static template = "awesome_gallery.GalleryRenderer";
    static props = {
        model: GalleryModel,
    }
    static components = { GalleryImage };
}
