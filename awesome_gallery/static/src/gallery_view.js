import { registry } from "@web/core/registry";

import { GalleryArchParser } from "./gallery_arch_parser/gallery_arch_parser";
import { GalleryController } from "./gallery_controller/gallery_controller";
import { GalleryModel  } from "./gallery_model";
import { GalleryRenderer } from "./gallery_renderer/gallery_renderer";


export const galleryView = {
    type: "gallery",
    display_name: "Gallery",
    icon: "fa fa-picture-o",
    multiRecord: true,
    Model: GalleryModel,
    Controller: GalleryController,
    Renderer: GalleryRenderer,
    ArchParser: GalleryArchParser,

    props(genericProps, view) {
        const { ArchParser } = view;
        const { arch } = genericProps;
        const archInfo = new ArchParser().parse(arch);

        return {
            ...genericProps,
            Model: view.Model,
            Renderer: view.Renderer,
            archInfo,
        };
    },
};

registry.category("views").add("gallery", galleryView);
