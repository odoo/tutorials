/** @odoo-module */

import { Component } from "@odoo/owl";
import { GalleryModel } from "./gallery_model";

export class GalleryRenderer extends Component {
    static template = "awesome_gallery.GalleryRenderer";
    static props = {
        model: GalleryModel,
    }
}
