/** @odoo-module */
import {Layout} from "@web/search/layout";
import {useService} from "@web/core/utils/hooks";
import { usePager } from "@web/search/pager_hook";

const {Component, onWillStart, onWillUpdateProps, useState} = owl;


export class GalleryController extends Component {
    static template = "awesome_gallery.View";
    static components = {Layout};

    setup() {
        this.orm = useService("orm");
        this.model = useState(
            new this.props.Model(
                this.orm,
                this.props.resModel,
                this.props.domain,
                this.props.fields,
                this.props.archInfo)
        );

        usePager( () => {
           return {
                limit: this.model.pager.limit,
                offset: this.model.pager.offset,
                total: this.model.recordsLength,
                onUpdate: async ({offset, limit}) => {
                     this.model.pager.offset = offset;
                     this.model.pager.limit = limit;
                     await this.model.load();
                }
           }
        });

        onWillStart(async () => {
            await this.model.load();
        });

        onWillUpdateProps(async (nextProps) => {
            if (JSON.stringify(nextProps.domain) !== JSON.stringify(this.props.domain)) {
                this.model.domain = nextProps.domain;
                await this.model.load();
            }
        });
    }

}
