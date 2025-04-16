from dataclasses import dataclass
from typing import Optional

from app.domain.model.file import Video
from app.domain.model.templates import SlideTemplate, TemplateField, TemplateFieldType


@dataclass
class Video(SlideTemplate):

    title: str = "Video"
    subtitle: str = "Subtitle"
    text_color: str = "#fff"
    video: Optional[Video] = None
    controls: bool = False
    loop: bool = True
    autoplay: bool = True

    def __post_init__(self):
        self.name = "Video"
        self.description = "A video slide"
        self.fields = [
            TemplateField(TemplateFieldType.TEXT, name=f"v_title", content=self.title),
            TemplateField(TemplateFieldType.TEXT, name=f"v_subtitle", content=self.subtitle),
            TemplateField(TemplateFieldType.COLOR, name=f"v_text_color", content=self.text_color),
            TemplateField(TemplateFieldType.VIDEO, name=f"v_video", content=self.video),
            TemplateField(TemplateFieldType.BOOL, name=f"v_controls", content=self.controls),
            TemplateField(TemplateFieldType.BOOL, name=f"v_loop", content=self.loop),
            TemplateField(TemplateFieldType.BOOL, name=f"v_autoplay", content=self.autoplay),
        ]

    @property
    def style(self) -> str:
        return f"""
h1.video-{self.id} {{
    font-size: 5em;
    font-size: 3rem;
    margin-bottom: 0.2rem;
    color: $v_text_color;
    text-shadow: 0 0 10px #000;
}}
p.video-{self.id} {{
    font-size: 2rem;
    color: $v_text_color;
    max-width: 800px;
    margin: 0 auto;
    margin-bottom: 3rem;
}}
div.video-{self.id} {{
    border-radius: 4px;
    padding: 2rem 0;
    margin: 0 0 2vh;
    background-color: #000000;
}}
div.video-{self.id} > video {{
    width: 100%;
    height: 60vh;
}}
"""

    @property
    def script(self) -> str:
        return f"""
document.addEventListener('DOMContentLoaded', function() {{
    document.addEventListener('keyup', function(e) {{
        if (e.key == "Enter" ||
            e.code == "Enter" ||      
            e.keyCode == 13      
        ) {{
            e.preventDefault();
            let video = document.querySelector(`#slide_${{page}} div.video-{self.id} video`);
            if (!video) {{
                return;
            }}
            if (video.paused) {{
                console.log('Play video', '{self.id}')
                video.play();
            }} else {{
                console.log('Pause video', '{self.id}')
                video.pause();
            }}
        }}
    }});
    document.addEventListener('keyup', function(e) {{
        if (e.key == " " ||
            e.code == "Space" ||      
            e.keyCode == 32      
        ) {{
            e.preventDefault();
            let video = document.querySelector(`#slide_${{page}} div.video-{self.id} video`);
            if (video && {'true' if self.autoplay else 'false'}) {{
                console.log('Play video', '{self.id}')
                video.play();
                return;
            }}
            video = document.querySelector(`#slide_${{page - 1}} div.video-{self.id} video`);
            if (!video) {{
                return;
            }}
            console.log('Pause video', '{self.id}')
            video.pause();
         }}
    }});
}});"""

    @property
    def content(self) -> str:
        return f"""<h1 class="video-{self.id}">$v_title</h1>
<p class="video-{self.id}">$v_subtitle</p>
<div class="video-{self.id}">
    <video src="$v_video"{" controls" if self.controls else ""}{" loop" if self.loop else ""}>The video tag is not supported by your browser</video>
</div>
"""
