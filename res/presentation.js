let page = 0;
document.addEventListener('DOMContentLoaded', function() {
    const total_pages = $total_pages_count;
    document.querySelector('#current-page').innerHTML = page + 1;
    document.querySelector('#total-pages').innerHTML = total_pages;
    const firstSlide = document.querySelector(`#slide_0`);
    firstSlide.scrollIntoView({
        behavior: 'smooth'
    });

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
        const targetSlide = document.querySelector(`#slide_${page}`);
        targetSlide.scrollIntoView({
            behavior: 'smooth'
        });
        document.querySelector('#current-page').innerHTML = page + 1;
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
            const targetSlide = document.querySelector(`#slide_${page}`);
            targetSlide.scrollIntoView({
                behavior: 'smooth'
            });                
            document.querySelector('#current-page').innerHTML = page + 1;
        });
    });
});
$scripts
$slides_scripts
