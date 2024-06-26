/** @odoo-module **/

import { Component, onWillStart, onWillUpdateProps, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { standardViewProps } from "@web/views/standard_view_props";

export class GalleryController extends Component {
    static components = { Layout };
    static template = "awesome_dashboard.GalleryController";
    static props = {
        ...standardViewProps,
        image_field: true,
        Model: Object,
        Renderer: Object,
    };

    setup() {
        this.model = useState(new this.props.Model(useService("orm"), this.props.archInfo, this.props.resModel));

        onWillStart(() => {
            this.model.loadNewImages([]);
        });

        onWillUpdateProps(() => {
            this.model.loadNewImages([]);
        });
    }
}
