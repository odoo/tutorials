/** @odoo-module **/

import { Component, onWillStart, onWillUpdateProps, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { standardViewProps } from "@web/views/standard_view_props";
import { usePager } from "@web/search/pager_hook";
import { useModel } from "@web/model/model";

export class GalleryController extends Component {
    static components = { Layout };
    static template = "awesome_dashboard.GalleryController";
    static props = {
        ...standardViewProps,
        image_field: true,
        Model: Object,
        Renderer: Object,
    };

    async setup() {
        this.model = useState(new this.props.Model(useService("orm"), this.props.archInfo, this.props.resModel));

        usePager(() => {
            return {
                offset: this.model.pagerState.offset,
                limit: this.model.pagerState.limit,
                total: this.model.recordsLength,
                onUpdate: async ({ offset, limit }) => {
                    this.model.pagerState.offset = offset;
                    this.model.pagerState.limit = limit;
                    console.log("Offset: ", offset, " Limit: ", limit);
                    await this.model.loadNewImages([]);
                },
            };
        });

        onWillStart(() => {
            this.model.loadNewImages([]);
        });
    }
}
