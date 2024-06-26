/** @odoo-module **/

import { Component } from "@odoo/owl";
import { url } from "@web/core/utils/urls";
import { useService } from "@web/core/utils/hooks";

export class GalleryImage extends Component {
    static template = "awesome_dashboard.GalleryImage";
    static props = {
        state: Object,
        image: Object,
    };

    setup() {
        this.action = useService("action");
    }

    openForm() {
        this.action.switchView("form");
    }

    getImageUrl(imageId) {
        console.log(this);

        const { resModel, archInfo } = this.props.state;
        return url("/web/image", {
            model: resModel,
            id: imageId,
            field: archInfo.image_field,
        });
    }
}
