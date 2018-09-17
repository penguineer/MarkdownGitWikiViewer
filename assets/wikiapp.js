function switch_page(page) {
    window.history.pushState("object or string", page, '/wiki'+page);
    document.title = page;

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var md = new Remarkable();
            var html = md.render(this.responseText)

            document.getElementById("content").innerHTML = html;
        }
    };
    xhttp.open("GET", '/data'+page, true);
    xhttp.send();

}

function load_structure() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            var html = this.responseText

            document.getElementById("structure").innerHTML = html;
        }
    };
    xhttp.open("GET", '/structure', true); // load synchronous
    xhttp.send();
}

function load_content_by_url() {
    var wiki_re = new RegExp("^http://.*/wiki(/.*$)")
    match = wiki_re.exec(document.URL)
    if (match) {
        page = match[1]
        switch_page(page)
    }
}

window.onpopstate = function(e){
    if(e.state){
        document.getElementById("content").innerHTML = e.state.html;
        document.title = e.state.pageTitle;
    }
    load_content_by_url();
};

window.onload = function(){
    load_structure();
    load_content_by_url();
}
