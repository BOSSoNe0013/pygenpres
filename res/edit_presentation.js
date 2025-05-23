/**
    PyGenPres - A Python Presentation Generator

    Copyright (C) 2025  Cyril BOSSELUT

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
**/

import {
    w2ui,
    w2utils,
    w2layout,
    w2toolbar,
    w2sidebar,
    w2form,
    w2confirm,
    query
} from 'https://rawgit.com/vitmalina/w2ui/master/dist/w2ui.es6.min.js';
window.w2ui = w2ui;
window.w2utils = w2utils;
const presId = '$presentation_id';
const presTitle = '$presentation_title';
const presFooter = '$presentation_footer';
const fontFamilies = [
    { id: 'Bebas Neue', text: 'Bebas Neue', style:"font-family: 'Bebas Neue';" },
    { id: 'Cookie', text: 'Cookie', style:"font-family: 'Cookie';" },
    { id: 'Indie Flower', text: 'Indie Flower', style:"font-family: 'Indie Flower';" },
    { id: 'Inter', text: 'Inter', style:"font-family: 'Inter';" },
    { id: 'Montserrat', text: 'Montserrat', style:"font-family: 'Montserrat';" },
    { id: 'Open Sans', text: 'Open Sans', style:"font-family: 'Open Sans';" },
    { id: 'Parisienne', text: 'Parisienne', style:"font-family: 'Parisienne';" },
    { id: 'Permanent Marker', text: 'Permanent Marker', style:"font-family: 'Permanent Marker';" },
    { id: 'Playfair Display', text: 'Playfair Display', style:"font-family: 'Playfair Display';" },
    { id: 'Poppins', text: 'Poppins', style:"font-family: 'Poppins';" },
    { id: 'Roboto', text: 'Roboto', style:"font-family: 'Roboto';" },
    { id: 'Roboto Serif', text: 'Roboto Serif', style:"font-family: 'Roboto Serif';" },
    { id: 'Special Gothic', text: 'Special Gothic', style:"font-family: 'Special Gothic';" },
    { id: 'Source Code Pro', text: 'Source Code Pro', style:"font-family: 'source Code Pro';" },
    { id: 'Winky Rough', text: 'Winky Rough', style:"font-family: 'Winky Rough';" },
];
let slides = [
    $slide_items
];
let sbNodes = [];
function storeConfig(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch {
        console.error('Could not store config:', key);
    }
};
function getConfig(key, default_value = null) {
    try {
        const storedValue = localStorage.getItem(key);
        if (storedValue !== null) {
                return JSON.parse(storedValue); // Convert the JSON string back into an object or array
        }
        return default_value;
    } catch {
        console.error('Could not get config:', key);
        return default_value;
    }
};
function delConfig(key) {
    try {
        localStorage.removeItem(key);
    } catch {
        console.error('Could not delete config:', key);
    }
};
function useSystemTheme() {
    delConfig('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = prefersDark ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', theme);
};
function loadTheme() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const systemTheme = prefersDark ? 'dark' : 'light';
    const theme = getConfig('theme') || systemTheme;
    document.documentElement.setAttribute('data-theme', theme);
};
function capitalize(word) {
    if (typeof word !== 'string' || word.length === 0) {
        return word;
    }
    return word.charAt(0).toUpperCase() + word.slice(1);
};
loadTheme();
function genSbNodes() {
    if (slides.length > 0) {
        sbNodes = [...slides];
    }
    sbNodes.push({
        id: 'plus',
        text: 'Add slide',
        icon: 'fa fa-plus',
    });
};
genSbNodes();

let pstyle = 'border: 1px solid var(--border-color);overflow: hidden;';
let layout = new w2layout({
    name: 'main',
    box: '#content',
    panels: [
        { type: 'top', size: 40, resizable: false, style: pstyle, html: 'top'},
        { type: 'left', size: 150, resizable: false, style: pstyle, html: 'left'},
        { type: 'main', html: 'main', style: pstyle},
        { type: 'right', size: 250, resizable: false, style: pstyle, html: 'right'},
    ],
});
let right_layout = new w2layout({
    name: 'right_box',
    box: '#layout_main_panel_right .w2ui-panel-content',
    panels: [
        { type: 'main', html: 'main-right sb', style: pstyle},
        { type: 'bottom', size: 40, resizable: false, style: pstyle, html: 'bottom-right sb'},
    ],
});
let right_bottom_toolbar = new w2toolbar({
    name: 'right_bottom',
    box: '#layout_right_box_panel_bottom .w2ui-panel-content',
    items: [
        {
            type: 'button',
            id: 'delete',
            icon: 'fa fa-trash',
            text: 'Delete slide',
        },
    ],
});
right_bottom_toolbar.on('click', event => {
w2confirm('Are you sure?')
    .yes(() => {
        w2utils.lock('body', 'Removing slide...', true);
        const slideId = event.detail.item.slide_id;
        const url = `/s/${presId}/${slideId}.json`;
        const options = {
            method: 'DELETE',
            headers: {},
        };
        fetch(url, options)
            .then(resp => resp.json())
            .then(data => {
                console.log('data', data);
                window.location.reload();
            })
            .catch(error => {
                console.error(error);
                w2utils.unlock('body');
            });
    });
});
let toolbar = new w2toolbar({
    name: 'top',
    box: '#layout_main_panel_top .w2ui-panel-content',
    items: [
        {
            type: 'button',
            id: 'home',
            icon: 'fa fa-home',
        },
        { 
            type: 'input', 
            id: 'title', 
            placeholder: 'Enter title', 
            value: presTitle,
            input: { style: 'width: 25vw;min-width: 320px;' },
        },
        { 
            type: 'input', 
            id: 'footer', 
            placeholder: 'Enter footer text', 
            value: presFooter,
            input: { style: 'width: 25vw;min-width: 320px;' },
        },
        {
            type: 'spacer',
        },
        {
            type: 'menu',
            id: 'menu',
            text: 'Download',
            icon: 'fa fa-download',
            items: [
                { id: 'dl-html', text: 'HTML', icon: 'fa fa-file-code' },
                { id: 'dl-pdf', text: 'PDF', icon: 'fa fa-file-pdf' }
            ],
        },
        {
            type: 'menu-radio',
            id: 'theme',
            icon(item) {return item.get(item.selected)?.icon},
            text(item) {return item.get(item.selected)?.text},
            selected: getConfig('theme') || 'system',
            items: [
                { id: 'system', text: 'System', icon: 'fa fa-circle-half-stroke'},
                { id: 'light', text: 'Light', icon: 'fa fa-sun'},
                { id: 'dark', text: 'Dark', icon: 'fa fa-moon'},
            ],
        }
    ],
});
function updatePresentation(data, callback) {
    console.log('updatePresentation', data);
    let url = '/save';
    let options = w2utils.prepareParams(url, {
        method: 'POST',
        headers: {},
        body: data,
    }, 'JSON');
    fetch(url, options)
        .then(resp => resp.json())
        .then(json => {
            console.log('updatedPresentation', json);
            if (typeof callback === 'function') {
                callback();
            }
            w2utils.unlock('body');
            if (window.location.href.endsWith('/new')) {
                const id = json['id'];
                window.location.href = `/edit/${id}`;
            }
        }).catch(error => {
            console.log(error);
            w2utils.unlock('body');
        });
};
toolbar.on('click', event => {
    console.log('Toolbar click', event);
    if (event.target === 'home') {
        window.location.replace(`/`);
    }
    else if (event.target === 'menu:dl-html') {
        fetch(`/p/${presId}.html`)
            .then(response => response.blob())
            .then(blob => {
                let url = URL.createObjectURL(blob);
                const tmp1 = document.createElement("a");
                tmp1.href = url;
                tmp1.download = `${presTitle}.html`;
                tmp1.click();
                URL.revokeObjectURL(url);
                tmp1.remove();
            });
    }
    else if (event.target === 'menu:dl-pdf') {
        let popup = window.open(`/p/${presId}.html`, 'Print', 'width=1280, height=720');
        setTimeout(() => { popup.print();}, 10000);
    }
    else if (event.target === 'theme:light') {
        storeConfig('theme', 'light');
        document.documentElement.setAttribute('data-theme', 'light');
    }
    else if (event.target === 'theme:dark') {
        storeConfig('theme', 'dark');
        document.documentElement.setAttribute('data-theme', 'dark');
    }
    else if (event.target === 'theme:system') {
        useSystemTheme();
    }
});
toolbar.on('change', event => {
    console.log('Toolbar change', event);
    if (['title', 'footer'].includes(event.target)) {
        w2utils.lock('body', 'Saving...', true);
        let data = {
            id: presId,
            changes: [
                {
                    field: event.target,
                    value: event.detail.value,
                }
            ]
        };
        updatePresentation(data);
    }
});
let slideForm = new w2form({
    name: 'slide_form',
    style: 'width: 100%;height: 100%; overflow: hidden auto;padding: 5px;',
    record: {},
    fields: [],
    onChange(event) {
        console.log('onChange', event.detail);
        w2utils.lock('body', 'Saving...', true);
        const slideId = this.record.id;
        const field = event.detail.field;
        let image_data = null;
        if (!field.startsWith('fx_') && field.endsWith('image') && event.detail.value.current.length > 0) {
            let entry = event.detail.value.current.at(0);
            image_data = {
                type: entry.type,
                name: entry.name,
                content: entry.content,
                size: entry.size
            };
        }
        let video_data = null;
        if (!field.startsWith('fx_') && field.endsWith('video') && event.detail.value.current.length > 0) {
            let entry = event.detail.value.current.at(0);
            video_data = {
                type: entry.type,
                name: entry.name,
                content: entry.content,
                size: entry.size
            };
        }
        let fx_value = null;
        if (field.startsWith('fx_') && event.detail.value.current.length > 0) {
            console.info('fx item', this.get(field).w2field.selected);
            fx_value = this.get(field).w2field.selected.id;
        };
        const value = field.endsWith('color') ?
            `#${event.detail.value.current}` : !field.startsWith('fx_') && field.endsWith('image') ?
                image_data : !field.startsWith('fx_') && field.endsWith('video') ?
                    video_data : field == 'theme' ?
                        event.detail.value.current.toLowerCase().replaceAll(' ', '_') : field.startsWith('fx_') ?
                            fx_value : event.detail.value.current;
        const data = {
            id: presId,
            changes: [
                {
                    field: 'slide',
                    id: slideId,
                    value: [
                        {
                            field: field,
                            value: value,
                        }
                    ]
                }
            ]
        };
        console.log('onChange', data);
        updatePresentation(data, () => {
            loadSlide(slideId);
        });
    },
});
function renderSlideForm(data) {
    console.log('renderSlideForm', data);
    if (typeof data.detail === 'string') {
        return;
    }
    w2ui.slide_form.fields = [
        {
            field: 'id',
            type: 'text',
            hidden: 'hidden'
        },
        {
            field: 'title',
            type: 'text',
            html: {
                span: -1,
                label: 'Name',
                group: 'Slide info',
                groupCollapsible: true
            }
        },
        {
            field: 'description',
            type: 'textarea',
            html: {
                span: -1,
                label: 'Description'
            }
        },
        {
            field: 'header_alignment',
            type: 'list',
            options: {
                items: [
                    { id: 'left', text: 'Left' },
                    { id: 'center', text: 'Center' },
                    { id: 'right', text: 'Right' },
                ]
            },
            html: { span: -1, label: 'Header alignment', group: 'General', groupCollapsible: true}
        },
        {
            field: 'header_font_family',
            type: 'list',
            options: {
                items: fontFamilies
            },
            html: { span: -1, label: 'Header font family'}
        },
        {
            field: 'font_family',
            type: 'list',
            options: {
                items: fontFamilies
            },
            html: { span: -1, label: 'Font family'}
        },
        { field: 'accent_color', type: 'color', html: { span: -1, label: 'Accent color' } },
        {
            field: 'background_color',
            type: 'color',
            html: {
                span: -1,
                label: 'Background color',
                group: 'Background',
                groupCollapsible: true
            }
        },
        {
            field: 'background_color_alt',
            type: 'color',
            html: {
                span: -1, label: 'Alternate background color'
            }
        },
        {
            field: 'background_image',
            type: 'file',
            options: {
                max: 1,
                maxItemWidth: 160
            },
            html: {
                span: -1,
                label: 'Background image',
                style: 'height: 86px;'
            }
        },
        {
            field: 'transition',
            type: 'list',
            options: {
                url: '/tr',
                minLength: 0
            },
            html: {
                span: -1,
                label: 'Model',
                group: 'Transition',
                groupCollapsible: true
            }
        },
        {
            field: 'duration',
            type: 'float',
            options: {
                min: 0,
                max: 2,
                step: 0.1,
                suffix: 's',
                keyboard: false
            },
            html: {
                span: -1,
                label: 'Duration'
            }
        },
        {
            field: 'template',
            type: 'list',
            options: {
                url: '/t',
                minLength: 0
            },
            html: {
                span: -1,
                label: 'Model',
                group: 'Template',
                groupCollapsible: true
            }
        },
        {
            field: 'theme',
            type: 'combo',
            options: {
                url: '/th',
                minLength: 0
            },
            html: {
                span: -1,
                label: 'Theme'
            }
        },
    ];
    w2ui.slide_form.record = {
        id: data.id,
        title: data.title,
        description: data.description,
        header_font_family: data.header_font_family,
        font_family: data.font_family,
        header_alignment: data.header_alignment,
        accent_color: data.accent_color.replace('#', '').toUpperCase(),
        background_color: data.background_color.replace('#', '').toUpperCase(),
        background_color_alt: data.background_color_alt.replace('#', '').toUpperCase(),
        background_image: data.background_image,
        transition: { id: data.transition.name.toLowerCase().replaceAll(' ', '_'), text: data.transition.name },
        duration: data.transition.duration,
        template: { id: data.template.name.toLowerCase().replaceAll(' ', '_'), text: data.template.name },
        theme: { id: data.theme, text: data.theme.split('_').map(word => capitalize(word)).join(' ') },
    };
    data.template.fields.forEach(field => {
        let type = 'text';
        let value = field.content;
        let style = '';
        let options = {};
        if (field.type === 'image' || field.type === 'video') {
            type = 'file';
            style = 'height: 86px;';
            options = { 
                max: 1,
                maxItemWidth: 160
            };
            if (value === '') {
                value = null;
            }
        }
        else if (field.type === 'color') {
            type = 'color';
            value = field.content.replace('#', '').toUpperCase();
        }
        else if (field.type === 'markdown') {
            type = 'textarea';
        }
        else if (field.type === 'bool') {
            type = 'toggle';
        }
        w2ui.slide_form.fields.push({
            field: 't_' + field.name,
            type: type,
            options: options,
            html: { span: -1, label: field.name.split('_').join(' '), style: style }
        });
        w2ui.slide_form.record['t_' + field.name] = value;
        if (['text', 'markdown', 'image', 'video', 'iframe'].includes(field.type)) {
            const url = field.type === 'text' ? `/fx` : `/fx?target=element`;
            w2ui.slide_form.fields.push({
                field: 'fx_' + field.name,
                type: 'combo',
                options: {
                    url: url,
                    minLength: 0
                },
                html: {
                    span: -1,
                    label: field.name + ' fx',
                    attr: 'data-type="fx" placeholder="Select fx"',
                    text: `<button type="button" class="button-clear-input" data-target="fx_${field.name}">X</button>`
                }
            });
            const record = field.fx !== null ? {id: field.fx.id, text: field.fx.name} : '';
            w2ui.slide_form.record['fx_' + field.name] = record;
        }
    });
    w2ui.slide_form.formHTML = w2ui.slide_form.generateHTML();
    w2ui.slide_form.render('#layout_right_box_panel_main .w2ui-panel-content');

    let expanded_groups = getConfig('expanded-groups', ['Template']);
    w2ui.slide_form.toggleGroup('Slide info', expanded_groups.includes('Slide info'));
    w2ui.slide_form.toggleGroup('General', expanded_groups.includes('General'));
    w2ui.slide_form.toggleGroup('Background', expanded_groups.includes('Background'));
    w2ui.slide_form.toggleGroup('Transition', expanded_groups.includes('Transition'));
    w2ui.slide_form.toggleGroup('Template', expanded_groups.includes('Template'));

    document.querySelectorAll('.w2ui-group-title').forEach(elem => {
        elem.addEventListener('click', event => {
            if (elem.firstChild.classList.contains('w2ui-icon-collapse')){
                expanded_groups.push(elem.textContent);
            }
            else {
                expanded_groups.pop(elem.textContent);
            }
            storeConfig('expanded-groups', expanded_groups);
        })
    });
    document.querySelectorAll('.button-clear-input').forEach(button => {
        button.addEventListener('click', event => {
            const target = event.target.getAttribute('data-target');
            console.log('target', target);
            const target_input = document.getElementById(target);
            if (target_input !== null) {
                console.info(target_input.value);
                target_input.focus();
                target_input.value = '';
                target_input.blur();
                target_input.dispatchEvent(new Event('change'));
            }
        });
    });
};
function loadSlide(slideId) {
    console.log('Load slide', slideId);
    if (typeof slideId === 'undefined' || slideId === null || slideId.length === 0) {
        layout['load']('main' , '/static/no_slide_template.html');
        right_layout['load']('main' , '/static/no_slide_template.html');
        right_bottom_toolbar.disable('delete');
        return;
    }
    layout['load']('main' , `/s/${presId}/${slideId}.html`);
    right_bottom_toolbar.items[0].slide_id = slideId;
    right_bottom_toolbar.enable('delete');
    const url = `/s/${presId}/${slideId}.json`;
    const options = {
        method: 'GET',
        headers: {},
    };
    fetch(url, options)
        .then(resp => resp.json())
        .then(data => {
            console.log('data', data);
            if (typeof data.detail === 'string') {
                return;
            }
            renderSlideForm(data);
            w2ui.left.nodes[data.position].text = data.title;
            w2ui.left.refresh();
        });
};
let leftSidebar = new w2sidebar({
    name: 'left',
    reorder: true,
    box: '#layout_main_panel_left .w2ui-panel-content',
    style: 'width: 100%;height: 100%; overflow: hidden auto;padding: 5px;',
    topHTML: '<strong>Slides</strong>',
    nodes: sbNodes,
    onClick(event) {
        if (event.target === 'plus') {
            console.info('Add slide');
            const url = `/s/${presId}/add`;
            const options = {
                method: 'GET',
                headers: {},
            };
            fetch(url, options)
                .then(resp => resp.json())
                .then(data => {
                    console.log('data', data);
                    const slide = data.slides[data.slides.length - 1];
                    slides.length = 0;
                    data.slides.forEach(s => {
                        slides.push({
                            id: s.id,
                            text: s.title,
                            order: s.position,
                            icon: 'fa fa-rectangle-list'
                        });
                    });
                    genSbNodes();
                    renderSlideForm(slide);
                    w2ui.left.nodes = sbNodes;
                    w2ui.left.refresh();
                });
            return;
        }
        loadSlide(event.target);
    },
    onDragStart(event) {
        if (event.target === 'plus') {
            event.preventDefault();
        }
    },
    onDragOver(event) {
        if (event.detail.append) {
            event.preventDefault();
        }
    },
    onReorder(event) {
        const slideId = event.target;
        console.log('Reorder', event.detail);
        const slide = this.nodes.find(slide => slide.id === slideId);
        let initial_position = this.nodes.indexOf(slide);
        let position = initial_position;
        if (event.detail.append) {
            position = slides.length - 1;
        }
        else {
            const before = this.nodes.find(slide => slide.id === event.detail.moveBefore);
            position = this.nodes.indexOf(before);
            if (position > initial_position) {
                position -= 1;
            }
        }
        if (position !== initial_position) {
            w2utils.lock('body', 'Saving...', true);
            console.log('move slide from', initial_position,'to', position);
            const data = {
                id: presId,
                changes: [
                    {
                        field: 'slide',
                        id: slideId,
                        value: [
                            {
                                field: 'position',
                                value: position,
                            }
                        ]
                    }
                ]
            };
            console.log('onChange', data);
            updatePresentation(data, () => {
                //loadSlide(slideId);
            });
        } 
    },
    async onRender(event) {
        await event.complete;
        console.log('Rendering sidebar complete');
        this.select('$first_slide_id');
        loadSlide('$first_slide_id');
    },
});