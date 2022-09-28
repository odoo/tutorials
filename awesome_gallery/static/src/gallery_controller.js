import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onWillUpdateProps, useState } from "@odoo/owl";
import { standardViewProps } from "@web/views/standard_view_props";
import { GalleryModel } from "./gallery_model";
import { GalleryRenderer } from "./gallery_renderer";

export class GalleryController extends Component {
    static template = "awesome_gallery.GalleryController";
    static props = {
        ...standardViewProps,
        archInfo: Object,
    };
    static components = { Layout, GalleryRenderer };

    setup() {
        this.orm = useService("orm");

        this.model = useState(
            new GalleryModel(
                this.orm,
                this.props.resModel,
                this.props.archInfo,
            )
        );
        onWillStart(async () => {
            await this.model.load(this.props.domain);
        });

        onWillUpdateProps(async (nextProps) => {
            if (JSON.stringify(nextProps.domain) !== JSON.stringify(this.props.domain)) {
                await this.model.load(nextProps.domain);
            }
        });
    }
}
