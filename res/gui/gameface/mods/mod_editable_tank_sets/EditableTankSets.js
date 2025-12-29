window.EditableTankSetsStatus = (window.EditableTankSetsStatus || []);

function info(arg) {
    window.EditableTankSetsStatus.push(arg);
    console.info(arg);
}

info('import libs');
//noinspection JSFileReferences
import {ModelObserver} from "../libs/model.js";
//noinspection JSFileReferences
import {pxToRem, remToPx} from "../libs/common.js";

if ('EditableTankSetsView' in window) {
    info(`panic! panic!`);
    throw new Error(`нельзя съесть шоколадку два раза...`)
}

const view = {
    list: null,
    title: null,
    VehicleFilterModel: null,
    EditableTankSetsModel: null
};
window.EditableTankSetsView = view;

function addHeightRem(el, add) {
    if (!el)return;

    const style = getComputedStyle(el);
    if (!style || !('height' in style)) {
        return;
    }

    let height = null;

    const remTest = /(.+)rem$/.exec(style.height);
    if (remTest) {
        height = parseFloat(remTest [1]);
    }

    const pxTest = /(.+)px$/.exec(style.height);
    if (pxTest) {
        height = pxToRem(parseFloat(pxTest [1]));
    }

    if (!height) return;

    el.style.height = `${Math.max(20, height + add)}rem`;
}

function findUI(added) {
    const popoverBody = (added || document).querySelector('div.FilterPopover_body_9e82b944');
    if (!popoverBody) {
        // info('no popover body found');
        return false;
    }
    const filterSections = popoverBody.querySelector('div.VerticalScroll_content_62cb6120');
    if (!filterSections) {
        // info('no popover filter sections found');
        return false;
    }

    var created = false;

    view.title = popoverBody.querySelector('#editableTankSetsTitle');
    if (!view.title) {
        info('create editableTankSetsTitle');
        view.title = dom('div', {id: 'editableTankSetsTitle', className: 'FormatText_db904f12 FilterPopover_category_aa274a28'});
        filterSections.appendChild(view.title);

        addHeightRem(popoverBody.querySelector('div.FilterPopover_scroll_bce24275'), 40);
        created = true;
    }

    view.list = popoverBody.querySelector('#editableTankSetsList');
    if (!view.list) {
        info('create editableTankSetsList');
        view.list = dom('div', {id: 'editableTankSetsList', className: 'FilterPopover_toggleContainer_c7079ba8 FilterPopover_toggleContainer__type_38a25c90'});
        filterSections.appendChild(view.list);
        created = true;
    }

    if (created) {
        updateUI();
    }

    return true;
}

function updateUI() {
    const model = view.EditableTankSetsModel;
    if (!model)return;

    if (view.title) {
        view.title.textContent = model.groupTitle;
    }
}

function dom(tagName, opts, ...children) {
    const element = document.createElement(tagName);
    Object.keys(opts).forEach(k => {
        const v = opts[k];
        if (k === 'text') {
            element.textContent = v;
        } else element[k] = v;
    });

    if (children) {
        children.forEach(child => element.appendChild(child));
    }
    return element;
}

function main() {
    view.ModelObserver = ModelObserver;

    // Create model observer
    const vehicleFilterModel = ModelObserver("VehicleFilterModelRef");
    const editableTankSetsModel = ModelObserver("EditableTankSetsRef");

    // Initialize UI logic once the engine is fully ready
    info('engine.whenReady');
    engine.whenReady.then(() => {
        // Keep button in sync with model changes (alerts count etc.)
        vehicleFilterModel.onUpdate(m => {
            // info(arguments);
            // window.VehicleFilterAddon.modelUpdate = new Date();
            view.VehicleFilterModel = m;
        });
        vehicleFilterModel.subscribe();

        // Keep button in sync with model changes (alerts count etc.)
        editableTankSetsModel.onUpdate(m => {
            console.info(`editableTankSetsModel.onUpdate`);
            view.EditableTankSetsModel = m;
            updateUI();
        });
        editableTankSetsModel.subscribe();

        findUI();
    });

    const observer = new MutationObserver((records) => {
        for (const record of records) {
            for (const addedNode of record.addedNodes) {
                if (findUI(addedNode)) {
                    break;
                }
            }
        }
    });

    observer.observe(document.body, {childList: true, subtree: true});
}

try {
    info('start main');
    main();
} catch (e) {
    info('error');
    info(e)
}
