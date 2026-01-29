import { registry } from "@web/core/registry";
import { GalleryArchParser, GalleryController } from "./gallery_controller";

export const galleryView = {
    type: "gallery",
    display_name: "GalleryView",
    icon: "oi oi-view-list",
    multiRecord: true,
    Controller: GalleryController,
    ArchParser: GalleryArchParser
}

registry.category("views").add("gallery", galleryView);
