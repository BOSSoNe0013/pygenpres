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
    document.querySelectorAll('slide').forEach(slide => {
        if (slide.id === `slide_${page}`) {
            slide.classList.remove('hidden');
        }
        else {
            slide.classList.add('hidden');
        }
    });
};
function scrollToSlide() {
    const targetSlide = document.querySelector(`#slide_${page}`);
    targetSlide.scrollIntoView({
        behavior: 'smooth'
    });
    document.documentElement.focus();
};
document.addEventListener("animationend", (event) => {
    console.log(event);
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
        }
        showSlide();
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
                page = total_pages - 1;
            }
            showSlide();
        });
    });
    showSlide();
});
$scripts
$slides_scripts
