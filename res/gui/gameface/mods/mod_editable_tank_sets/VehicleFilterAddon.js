window.VehicleFilterAddonStatus = [];

function info(arg) {
    window.VehicleFilterAddonStatus.push(arg);
}

info('import libs');
//noinspection JSFileReferences
import {ModelObserver} from "../libs/model.js";

function modifyFilterUI() {
    const popoverBody = document.querySelector('div.FilterPopover_body_9e82b944');
    if (!popoverBody) {
        info('no popover body found');
        return;
    }
    const filterSections = popoverBody.querySelector('div.VerticalScroll_content_62cb6120');
    if (!filterSections) {
        info('no popover filter sections found');
        return;
    }
    filterSections.appendChild(dom('div', {className: 'FormatText_db904f12 FilterPopover_category_aa274a28', text: 'Мои группы'}));
    filterSections.appendChild(dom('div', {className: 'FormatText_db904f12 FilterPopover_category_aa274a28', text: 'Мои группы'}));
}

function dom(tagName, opts, ...children) {
    const element = document.createElement(tagName);
    for (const opt in opts) {
        if (opt === 'text') {
            element.innerText = text;
        } else element[opt] = opts[opt];
    }

    if (children) {
        children.forEach(child => element.appendChild(child));
    }
    return element;
}
function main() {
    // Create model observer
    const vehicleFilterModel = ModelObserver("VehicleFilterModel");
    window.VehicleFilterAddon = {
        model: vehicleFilterModel
    };
    // Initialize UI logic once the engine is fully ready
    info('engine.whenReady');
    engine.whenReady.then(() => {
        // Keep button in sync with model changes (alerts count etc.)
        vehicleFilterModel.onUpdate(m => {
            info(arguments);
            window.VehicleFilterAddon.modelUpdate = new Date();
        });
        vehicleFilterModel.subscribe();

        modifyFilterUI();
    });
}

try {
    info('start main');
    main();
} catch (e) {
    info('error');
    info(e)
}
