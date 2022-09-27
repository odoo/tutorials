import { Layout } from "@web/search/layout";
import { Component } from "@odoo/owl";
import { standardViewProps } from "@web/views/standard_view_props";

export class GalleryController extends Component {
    static template = "awesome_gallery.GalleryController";
    static props = {
        ...standardViewProps,
    };
    static components = { Layout };
}
