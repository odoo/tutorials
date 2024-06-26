/** @odoo-module */

import { Component, onWillStart, useState, onWillUpdateProps } from "@odoo/owl";
import { standardViewProps } from "@web/views/standard_view_props";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { KeepLast } from "@web/core/utils/concurrency";


export class GalleryController extends Component {
    static template = "awesome_gallery.GalleryController";
    static components = { Layout };
    static props = {
        ...standardViewProps,
        archParser: Object,
    };

    setup() {
        this.orm = useService("orm");
        this.images = useState({ data: [] });

        this.keepLast = new KeepLast();

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
        return this.keepLast.add(this.orm.webSearchRead(this.props.resModel, domain, {
            limit: this.props.archParser.limit,
            specification: {
                [this.props.archParser.image_field]: {},
            },
            context: {
                bin_size: true,
            }
        }))
    }
}
