/** @odoo-module */

import { KeepLast } from "@web/core/utils/concurrency";
import { url } from "@web/core/utils/urls";

export class GalleryModel {
    constructor(orm, resModel, archInfo, fields) {
        this.orm = orm;
        this.resModel = resModel;
        const { imageField, limit, fieldsForTooltip } = archInfo;
        this.imageField = imageField;
        this.fieldsForTooltip = fieldsForTooltip;
        this.limit = limit;
        this.keepLast = new KeepLast();
        this.fields = fields;
        this.pager = { offset: 0, limit: limit };
    }

    async loadImages(domain) {
        const specification = {
            [this.imageField]: {},
            write_date: {},
        }
        for (const field of this.fieldsForTooltip) {
            specification[field] = {};
        }
        const { length, records } = await this.keepLast.add(
            this.orm.webSearchRead(this.resModel, domain, {
                limit: this.pager.limit,
                offset: this.pager.offset,
                specification,
                context: {
                    bin_size: true,
                }
            })
        );
        this.records = records;    
        this.recordsLength = length;
        
    }

    async uploadImage(record_id, image_binary, domain) {
        await this.orm.webSave(
            this.resModel,
            [record_id],
            {
                [this.imageField]: image_binary,
            },
            {
                specification: {},
            }
        )
        await this.loadImages(domain);
    }
}
