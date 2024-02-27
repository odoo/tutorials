/** @odoo-module */

import { Component } from "@odoo/owl";
import { GalleryModel } from "./gallery_model";
import { GalleryImage } from "./gallery_image";
import { createElement } from "@web/core/utils/xml";
import { xml } from "@odoo/owl";

export class GalleryRenderer extends Component {
    static template = "awesome_gallery.GalleryRenderer";
    static props = {
        model: GalleryModel,
        onImageUpload: Function,
        tooltipTemplate: {
            optional: true,
            type: Element
        }
    }
    static components = { GalleryImage };

    setup() {
        if(this.props.tooltipTemplate) {
            const fieldsToReplace = this.props.tooltipTemplate.querySelectorAll("field");

            for(const field of fieldsToReplace) {
                const fieldName = field.getAttribute("name");
                const t = document.createElement("t");
                t.setAttribute("t-esc", `record.${fieldName}`)
                field.replaceWith(t);
            }

            const tooltipHTML = createElement("t", [this.props.tooltipTemplate]).outerHTML;
            this.owlTooltipTemplate = xml`${tooltipHTML}`
        }
    }
}
