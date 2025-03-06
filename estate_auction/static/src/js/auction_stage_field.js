// /** @odoo-module **/

// import { Component, useState, onMounted } from "@odoo/owl";
// import { registry } from "@web/core/registry";
// import { useService } from "@web/core/utils/hooks";

// class AuctionStageField extends Component {
//     setup() {
//         this.rpc = useService("rpc");

//         // ✅ Log props to verify they exist
//         console.log("📌 AuctionStageField Props:", this.props);

//         // ✅ Ensure props exist and provide default values
//         const initialStage = this.props.initialStage || "template";
//         const isAuction = this.props.isAuction ?? false;
//         const recordId = this.props.recordId ?? 0;

//         this.state = useState({
//             auctionStage: initialStage,
//             showDropdown: false,
//             isAuction,
//             recordId,
//         });

//         onMounted(() => {
//             console.log("✅ Mounted: Auction Stage =", this.state.auctionStage);
//             this.updateButtonStyle();
//         });
//     }

//     setAuctionStage(stage) {
//         if (!stage) {
//             console.error("❌ Auction stage is undefined!");
//             return;
//         }
//         this.state.auctionStage = stage;
//         this.state.showDropdown = false;
//         this.updateButtonStyle();

//         // Send update to backend
//         if (this.state.recordId) {
//             this.rpc({
//                 model: "estate.property",
//                 method: "write",
//                 args: [[this.state.recordId], { auction_stage: stage }],
//             }).then(() => {
//                 console.log("✅ Stage updated in DB!");
//             }).catch(error => {
//                 console.error("❌ RPC Error updating stage:", error);
//             });
//         }
//     }

//     updateButtonStyle() {
//         const button = this.el?.querySelector("#auction_stage_button");
//         if (!button) {
//             console.error("❌ Button element not found!");
//             return;
//         }

//         button.classList.remove("btn-primary", "btn-warning", "btn-success");

//         if (this.state.auctionStage === "template") {
//             button.classList.add("btn-primary");
//         } else if (this.state.auctionStage === "in_progress") {
//             button.classList.add("btn-warning");
//         } else if (this.state.auctionStage === "sold") {
//             button.classList.add("btn-success");
//         }
//     }

//     get buttonText() {
//         return {
//             template: "Template",
//             in_progress: "In Progress",
//             sold: "Sold",
//         }[this.state.auctionStage] || "Template";
//     }
// }

// AuctionStageField.template = "estate.AuctionStageField";

// // ✅ Ensure the component is registered properly
// registry.category("fields").add("AuctionStageField", AuctionStageField);

// console.log("📌 AuctionStageField Component Registered!");
