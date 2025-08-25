// Initialize Quill editors
var snow = new Quill('#snow', { theme: 'snow' });
var bubble = new Quill('#bubble', { theme: 'bubble' });
new Quill("#full", { 
    bounds: "#full-container .editor", 
    modules: { 
        toolbar: [
            [{ font: [] }, { size: [] }], 
            ["bold", "italic", "underline", "strike"], 
            [{ color: [] }, { background: [] }], 
            [{ script: "super" }, { script: "sub" }], 
            [{ list: "ordered" }, { list: "bullet" }, { indent: "-1" }, { indent: "+1" }], 
            ["direction", { align: [] }], 
            ["link", "image", "video"], 
            ["clean"]
        ] 
    }, 
    theme: "snow" 
});

// Handle form submission for #snow
var form = document.querySelector('.form');
form.addEventListener('submit', function() {
    var htmlContent = snow.root.innerHTML;
    document.getElementById('description-html').value = htmlContent;
});
