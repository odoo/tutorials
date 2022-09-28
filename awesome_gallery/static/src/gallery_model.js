import { KeepLast } from "@web/core/utils/concurrency";

export class GalleryModel {
    constructor(orm, resModel, archInfo) {
        this.orm = orm;
        this.resModel = resModel;
        const { imageField, limit } = archInfo;
        this.imageField = imageField;
        this.limit = limit;
        this.keepLast = new KeepLast();
    }

    async load(domain) {
        const { records } = await this.keepLast.add(
            this.orm.webSearchRead(this.resModel, domain, {
                limit: this.limit,
                specification: {
                    [this.imageField]: {},
                },
                context: {
                    bin_size: true,
                }
            })
        );
        this.records = records;
    }
}
