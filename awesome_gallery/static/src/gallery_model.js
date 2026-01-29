export class GalleryModel {
    constructor(orm, resModel, archInfo) {
        this.orm = orm;
        this.resModel = resModel;
        this.records = [];

        const { imageField, limit } = archInfo;
        this.imageField = imageField;
        this.limit = limit;
    }

    async load(domain) {
        const { records } = await this.orm.webSearchRead(
            this.resModel,
            domain,
            {
                limit: this.limit,
                specification: {
                    [this.imageField]: {},
                },
                context: {
                    bin_size: true,
                }
            }
        );
        this.records = records;
    }
}
