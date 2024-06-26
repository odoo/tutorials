/** @odoo-module */

import { registry } from "@web/core/registry";
import { GalleryController } from "./gallery_controller.js";
import { GalleryArchParser } from "./arch_parser.js";

export const galleryView = {
      type: "gallery",
      display_name: "Gallery",
      icon: "fa fa-picture-o",
      multiRecord: true,
      Controller: GalleryController,
      ArchParser: GalleryArchParser,

      props(genericProps, view) {
            const { ArchParser } = view;
            const { arch } = genericProps;
            const archParser = new ArchParser().parse(arch);
    
            return {
                ...genericProps,
                archParser,
            };
        },
  };

registry.category("views").add("gallery", galleryView);
