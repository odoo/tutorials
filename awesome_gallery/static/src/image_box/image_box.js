import { url } from "@web/core/utils/urls";
import { Component } from "@odoo/owl";

export class ImageBox extends Component {
    static template = "awesome_gallery.ImageBox";

    static props = {
        image_id: Number
    }

    setup() {
        this.url = url("/web/image", {
            model: "res.partner",
            id: this.props.image_id,
            fieldName: 'avatar_128'
        });
    }
}
