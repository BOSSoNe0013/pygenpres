"""
This module defines the root endpoint for the API.
"""

async def get_root() -> str:
    """
    Returns the HTML content for the root page.
    """
    return """<html>
    <head>
        <link rel="stylesheet" type="text/css" href="https://rawgit.com/vitmalina/w2ui/master/dist/w2ui.css" />
        <link rel="stylesheet" type="text/css" href="/static/base.css" />
        <script src="http://ajax.googleapis.com/ajax/libs/jquery/3.5.0/jquery.min.js"></script>
    </head>
    <body>
        <main id="content"></main>
    </body>
    <script type="module">
    import { w2form, query } from 'https://rawgit.com/vitmalina/w2ui/master/dist/w2ui.es6.min.js'
    function loadTheme() {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const systemTheme = prefersDark ? 'dark' : 'light';
        const theme = localStorage.getItem('theme') || systemTheme;
        document.documentElement.setAttribute('data-theme', theme);
    };
    loadTheme();
    new w2form({
        name: 'form',
        box: '#content',
        style: 'max-width: 400px; margin: 20px auto;',
        pageStyle: 'display: flex; flex-direction: column; gap: 10px;',
        fields: [
            { field: 'pres', type: 'list',
                html: { label: 'Presentations' },
                options: { 
                    url: '/p',
                    minLength: 0,
                }
            },
        ],
        actions: {
            show() {
                if(typeof this.record.pres !== 'undefined') {
                    window.location.replace(`/p/${this.record.pres.id}.html`);
                }
            },
            edit() {
                if(typeof this.record.pres !== 'undefined') {
                    window.location.replace(`/edit/${this.record.pres.id}`);
                }
            },
            new() {
                window.location.replace(`/new`);
            }
        }
    });
    </script>
</html>"""
