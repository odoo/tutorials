/** @odoo-module */

import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onWillUpdateProps, useState } from "@odoo/owl";
import { standardViewProps } from "@web/views/standard_view_props";

export class GalleryController extends Component {
    static template = "awesome_gallery.GalleryController";
    static props = {
        ...standardViewProps,
        archInfo: Object,
    };
    static components = { Layout };

    setup() {
        this.orm = useService("orm");
        this.images = useState({ data: [] });
        onWillStart(async () => {
            const { records } = await this.loadImages(this.props.domain);
            this.images.data = records;
        });

        onWillUpdateProps(async (nextProps) => {
            if (JSON.stringify(nextProps.domain) !== JSON.stringify(this.props.domain)) {
                const { records } = await this.loadImages(nextProps.domain);
                this.images.data = records;
            }
        });
    }

    loadImages(domain) {
        return this.orm.webSearchRead(this.props.resModel, domain, {
            limit: this.props.archInfo.limit,
            specification: {
                [this.props.archInfo.imageField]: {},
            },
            context: {
                bin_size: true,
            }
        });
    }
}
