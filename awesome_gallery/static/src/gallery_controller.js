import {
    Component,
    onWillStart,
    onWillUpdateProps,
    useState,

} from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { standardViewProps } from "@web/views/standard_view_props";
import { SearchBar } from "@web/search/search_bar/search_bar";
import { usePager } from "@web/search/pager_hook";
import { GalleryModel } from "./gallery_model";
import { useService } from "@web/core/utils/hooks";

export class GalleryController extends Component {
    static template = "awesome_gallery.gallery_controller";
    static components = { Layout, SearchBar };
    static props = {
        ...standardViewProps,
        archInfo: Object,
    }


    setup() {
        this.action = useService("action");

        this.model = useState(
            new GalleryModel(
                this.props.resModel,
                this.props.archInfo.image_field,
                this.props.archInfo.tooltip_field,
                this.props.archInfo.limit
            )
        )

        usePager(() => {
            return {
                offset: this.model.pager.offset,
                limit: this.model.pager.limit,
                total: this.model.imagesLength,
                onUpdate: async ({ offset, limit }) => {
                    this.model.pager.offset = offset;
                    this.model.pager.limit = limit;
                    await this.model.loadImages(this.props.domain);
                },
            };
        });

        onWillStart(async () => {
            await this.model.loadImages(this.props.domain)
        })

        onWillUpdateProps(async (nextProps) => {
            if (JSON.stringify(nextProps.domain) !== JSON.stringify(this.props.domain))
                await this.model.loadImages(nextProps.domain)
        })
    }

    onImageClick(id) {
        this.action.switchView("form", { resId: id });
    }
}
