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

let page = 0;
function showSlide() {
    document.querySelector('#current-page').innerHTML = page + 1;
    const current_slide = document.querySelector('slide.current');
    document.querySelectorAll('slide').forEach(slide => {
        if (slide.id === `slide_${page}`) {
            slide.style.animationPlayState = 'running';
            document.querySelectorAll(`#${slide.id} *`).forEach(el => {
                el.style.animationPlayState = 'running';
            });
            slide.classList.remove('hidden');
            slide.classList.add('current');
        }
    });
    if (!document.querySelector('#presentation-container').classList.contains('first-load')) {
        current_slide.classList.remove('current');
        current_slide.classList.add('hidden');
    }
};
function scrollToSlide() {
    const targetSlide = document.querySelector(`#slide_${page}`);
    targetSlide.scrollIntoView({
        behavior: 'smooth'
    });
    document.documentElement.focus();
};
let cursorTimeout;
function hideCursor(elem) {
    elem.classList.add('no-cursor');
};
function showCursor(elem) {
    elem.classList.remove('no-cursor');
    clearTimeout(cursorTimeout);
    cursorTimeout = setTimeout(() => {
        hideCursor(elem);
    }, 1000);
};
document.addEventListener("animationend", (event) => {
    console.log(event);
    document.querySelector('#presentation-container').classList.remove('first-load');
    scrollToSlide();
});
document.scrollToSlide = scrollToSlide;
document.addEventListener('DOMContentLoaded', function() {
    const total_pages = $total_pages_count;
    document.querySelector('#total-pages').innerHTML = total_pages;

    document.addEventListener('keyup', function(e) {
        if (e.key == " " ||
            e.code == "Space" ||      
            e.keyCode == 32      
        ) {
            page += 1;
            if (page >= total_pages) {
                page = 0;
            }
            showSlide();
        }
    });
    document.querySelectorAll('slide').forEach(slide => {
        slide.addEventListener('mousemove', function(e) {
            showCursor(slide);
        });
        slide.addEventListener('click', function() {
            page += 1;
            if (page >= total_pages) {
                page = 0;
            }
            showSlide();
        });
    });
    var touch_moved = false;
    document.addEventListener('touchstart', function(e) {
        touch_moved = false;
    });
    document.addEventListener('touchmove', function(e) {
        touch_moved = true;
    });
    document.addEventListener('touchend', function(e) {
        if (!touch_moved) {
            page += 1;
            if (page >= total_pages) {
                page = 0;
            }
            showSlide();
        }
    });

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            if (e.target.href.endsWith("#next")) {
                page += 1;
                if (page >= total_pages) {
                    page = total_pages - 1;
                }
            }
            if (e.target.href.endsWith("#prev")) {
                page -= 1;
                if (page < 0) {
                    page = 0;
                }
            }
            if (e.target.href.endsWith("#first")) {
                page = 0;
            }
            if (e.target.href.endsWith("#last")) {
                if (page < total_pages - 2) {
                    const s = total_pages - 1 - page;
                    const ids = [...Array(s).keys()].map(i => i + page);
                    const slides = ids.map(id => document.querySelector(`#slide_${id}`));
                    slides.forEach(slide => {
                        slide.style.animationPlayState = 'running';
                        document.querySelectorAll(`#${slide.id} *`).forEach(el => {
                            el.style.animationPlayState = 'running';
                        });
                    });
                }
                page = total_pages - 1;
            }
            showSlide();
        });
    });
    showSlide();
});
$scripts
$slides_scripts
