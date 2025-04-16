document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('keyup', function(e) {
        if (e.key == "Enter" ||
            e.code == "Enter" ||      
            e.keyCode == 13      
        ) {
            e.preventDefault();
            let video = document.querySelector(`#slide_${page} div.video-$id video`);
            if (!video) {
                return;
            }
            if (video.paused) {
                console.log('Play video', '$id')
                video.play();
            } else {
                console.log('Pause video', '$id')
                video.pause();
            }
        }
    });
    document.addEventListener('keyup', function(e) {
        if (e.key == " " ||
            e.code == "Space" ||      
            e.keyCode == 32      
        ) {
            e.preventDefault();
            let video = document.querySelector(`#slide_${page} div.video-$id video`);
            if (video && $autoplay) {
                console.log('Play video', '$id')
                video.play();
                return;
            }
            video = document.querySelector(`#slide_${page - 1} div.video-$id video`);
            if (!video) {
                return;
            }
            console.log('Pause video', '$id')
            video.pause();
         }
    });
});
