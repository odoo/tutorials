/** @odoo-module **/

import { KeepLast } from "@web/core/utils/concurrency";

export class GalleryModel {
    constructor(orm, archInfo, resModel) {
        this.orm = orm;
        this.archInfo = archInfo;
        this.resModel = resModel;
        this.keepLast = new KeepLast();
        this.images = [];
        this.recordsLength = 0;
        this.pagerState = {
            offset: 0,
            limit: 10,
        };
    }

    async loadNewImages(domain) {
        this.images = await this.keepLast.add(this._loadImages(domain));
    }

    async _loadImages(domain) {
        let specs = {
            [this.archInfo.image_field]: {},
        };

        if (this.archInfo.tooltip_field) {
            specs[this.archInfo.tooltip_field] = {};
        }

        const { length, records } = await this.orm.webSearchRead(this.resModel, domain, {
            specification: specs,
            offset: this.pagerState.offset,
            limit: this.pagerState.limit,
            context: {
                bin_size: true,
            },
        });

        this.recordsLength = length;
        return records;
    }
}
