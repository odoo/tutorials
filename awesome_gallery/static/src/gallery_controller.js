import { Component, onWillStart, onWillUpdateProps, useState } from '@odoo/owl';
import { Layout } from '@web/search/layout';
import { standardViewProps } from "@web/views/standard_view_props";
import { useService } from '@web/core/utils/hooks';
import { usePager } from '@web/search/pager_hook';


export class GalleryController extends Component {
    static template = 'awesome_gallery.GalleryController';
    static components = { Layout };
    static props = {
        ...standardViewProps,
        Model: Function,
        Renderer: Function,
        archInfo: {
            type: Object,
            shape: {
                imageField: String,
                tooltipFields: Array,
                tooltipTemplate: Element
            }
        }
    };

    setup() {
        const orm = useService('orm');
        this.model = useState(new this.props.Model(
            this.props.resModel,
            orm,
            this.props.archInfo
        ));
        usePager(() => {
            return {
                offset: this.model.offset,
                limit: this.model.limit,
                total: this.model.total,
                onUpdate: async ({ offset, limit }) => {
                    this.model.offset = offset;
                    this.model.limit = limit;
                    await this.model.load(this.props.domain);
                    this.render(true);
                }
            };
        });
        const load = async () => {
            await this.model.load(this.props.domain);
        }
        onWillStart(load);
        onWillUpdateProps(load);
    }

    async uploadImage(id, data) {
        await this.model.uploadImage(id, data, this.props.domain);
    }
};
