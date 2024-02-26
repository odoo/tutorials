/** @odoo-module */

import { Component, onWillStart, onWillUpdateProps, useState } from "@odoo/owl";
import { standardViewProps } from "@web/views/standard_view_props";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout"



export class GalleryController extends Component {
    static template = "awesome_gallery.GalleryController";

    static props = {
        ...standardViewProps,
        archInfo: Object,
        Model: Function,
        Renderer: Function
    };

    static components = { Layout };

    setup() {
        this.orm = useService("orm");
        this.model = useState(new this.props.Model(this.orm, this.props.resModel, this.props.archInfo));
        
        onWillStart(async () => {
            await this.model.loadImages(this.props.domain);
        });

        onWillUpdateProps(async (nextProps) => {
            if (JSON.stringify(nextProps.domain) !== JSON.stringify(this.props.domain)) {
                await this.model.loadImages(nextProps.domain);
            }
        });
    }
}
