window.EditableTankSetsStatus = (window.EditableTankSetsStatus || []);

function info(arg) {
    window.EditableTankSetsStatus.push(arg);
    console.info(arg);
}

info('import libs');
//noinspection JSFileReferences
import {ModelObserver} from "../libs/model.js";
import {pxToRem, remToPx} from "../libs/common.js";
import {showTooltip, hideTooltip} from "../libs/views.js";
//noinspection JSFileReferences

if ('EditableTankSetsView' in window) {
    info(`panic! panic!`);
    throw new Error(`нельзя съесть шоколадку два раза...`)
}

const view = {
    /**
     @type {HTMLDivElement}
     */
    list: null,
    title: null,
    VehicleFilterModel: null,

    listDisplay: null,
    titleDisplay: null
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

function disposeUI(removed) {
    if (!removed) return;

    if (view.title && !document.body.contains(view.title)) {
        view.title = null;
    }
    if (view.list && !document.body.contains(view.list)) {
        view.list = null;
    }
}

function restoreUI(added) {
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
        view.titleDisplay = null;
        filterSections.appendChild(view.title);

        addHeightRem(popoverBody.querySelector('div.FilterPopover_scroll_bce24275'), 50);
        created = true;
    }

    view.list = popoverBody.querySelector('#editableTankSetsList');
    if (!view.list) {
        info('create editableTankSetsList');
        view.list = dom('div', {id: 'editableTankSetsList', className: 'FilterPopover_toggleContainer_c7079ba8 FilterPopover_toggleContainer__type_38a25c90'});
        view.listDisplay = null;
        filterSections.appendChild(view.list);
        created = true;
    }

    if (created) {
        updateUI();
    }

    return true;
}

const ActiveButtonClass = 'Toggle_cdf77db0 Toggle_base__theme-primary_3e3de333 Toggle_base__activated_d584e080 FilterPopover_toggle_747f4b53 FilterPopover_toggle__activated_19a04a6d';
const InactiveButtonClass = 'Toggle_cdf77db0 Toggle_base__theme-primary_3e3de333 FilterPopover_toggle_747f4b53';

function updateUI() {
    if (!view.VehicleFilterModel) return;

    const model = view.VehicleFilterModel.EditableTankSets;

    if (view.title && view.titleDisplay != model.groupTitle) {
        view.titleDisplay = model.groupTitle;

        view.title.textContent = model.groupTitle;
    }

    if (view.list && view.listDisplay != model.collections) {
        view.listDisplay = model.collections;

        while (view.list.firstChild)
            view.list.removeChild(view.list.firstChild);

        /**
         <div class="Toggle_cdf77db0 Toggle_base__theme-primary_3e3de333 FilterPopover_toggle_747f4b53" data-name="Toggle">
         <div class="Toggle_border_3d0d0d39"></div>
         <div class="Toggle_background_78cd67c0"></div>
         <div class="Toggle_bulb_fe6d0fba"></div>
         <div class="Toggle_overlay_e2999686"></div>
         <div class="Toggle_content_17eff4d2">
         <div class="FilterPopover_specialsIcons_5a3d8e7" style="background-image: url(img://uri.png); background-repeat: no-repeat no-repeat; background-size: contain; background-position-x: 50.000000%; background-position-y: 50.000000%; " src="img://gui/maps/icons/hangar/filter/special/bonus.png"></div>
         </div>
         </div>

         icon path: img://gui/maps/icons/../maps/icons/mod_editable_tank_sets/1.png
         image path: img://gui/maps/icons/hangar/filter/special/bonus.png
         */

        const collections = JSON.parse(model.collections);
        collections.forEach(collection => {
            const n = collection.n;
            const button =
                dom('div', {dataCollection: n, className: collection.active ? ActiveButtonClass : InactiveButtonClass},
                    dom('div', {className: 'Toggle_border_3d0d0d39'}),
                    dom('div', {className: 'Toggle_background_78cd67c0'}),
                    dom('div', {className: 'Toggle_bulb_fe6d0fba'}),
                    dom('div', {className: 'Toggle_overlay_e2999686'}),
                    dom('div', {className: 'Toggle_content_17eff4d2'},
                        dom('div', {className: 'VehicleLevel_3c938122 FilterPopover_vehicleLevel_41885117', text: `${n}`})
                    ),
                );
            button.onclick = function () {
                toggleCollection(n);
            };
            button.onmouseenter = function () {
                showTooltip(collection.title);
            };
            button.onmouseleave = function () {
                hideTooltip();
            };
            view.list.appendChild(button);
        });
    }
}

function toggleCollection(n) {
    console.info(`toggle collection ${n}`);

    const model = view.VehicleFilterModel;
    if (!model) return;

    const collections = JSON.parse(model.EditableTankSets.collections);
    for (const c of collections) {
        if (c.n === n) {
            c.active = !c.active;
            console.info(`collection.${n}.active=${c.active}`)
        }
    }

    const actives = collections
        .filter(e => e.active)
        .map(e => e.n);

    model.EditableTankSets.collections = JSON.stringify(collections);
    model.EditableTankSets.onSave({"actives": JSON.stringify(actives)});
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

    // Initialize UI logic once the engine is fully ready
    info('engine.whenReady');
    engine.whenReady.then(() => {
        // Keep button in sync with model changes (alerts count etc.)
        vehicleFilterModel.onUpdate(m => {
            // info(arguments);
            // window.VehicleFilterAddon.modelUpdate = new Date();
            view.VehicleFilterModel = m;
            updateUI();
        });
        vehicleFilterModel.subscribe();

        restoreUI(null);
    });

    const observer = new MutationObserver((records) => {
        for (const record of records) {
            for (const node of record.addedNodes) {
                if (node.nodeType === 1 && restoreUI(node)) {
                    break;
                }
            }
            for (const node of record.removedNodes) {
                if (node.nodeType === 1 && disposeUI(node)) {
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
