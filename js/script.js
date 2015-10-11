
// Function to navigate to coordinate in papaya viewer
function move_coordinate(x,y,z) {
    var coor = new papaya.core.Coordinate();
    papayaContainers[0].viewer.getIndexCoordinateAtWorld(parseFloat(x), parseFloat(y), parseFloat(z), coor);
    papayaContainers[0].viewer.gotoCoordinate(coor);
}

// Rendering function

function export_svg() {

    $("#canvas-svg").remove()
    var cx = $($("canvas")[0]).get(0).getContext("2d");
    var image = cx.canvas.toDataURL("image/png");
    var svgimg = document.createElementNS("http://www.w3.org/2000/svg", "image");
    svgimg.setAttributeNS("http://www.w3.org/1999/xlink", 'xlink:href', image);
    CanvasToSVG.convert(cx.canvas, svgimg);
    document.getElementById('export').href = svgimg.firstChild.imageData;
    $("#svgexport").append($("<img src='" + svgimg.firstChild.imageData+ "' alt='file.svg' id='canvas-svg'>"));
    $('#exportmodal').modal('toggle');
    $('.modal-backdrop').remove();

}

function load_images(brainmaps){

    // Generate initial table, and buttons for nidm
    image_files =  [];
    image_names = [];
    for (var brainmap in brainmaps) {
	if (brainmaps.hasOwnProperty(brainmap)) {
	    image_files.push(brainmaps[brainmap].replace("file://","").replace("./",""))
            var image_name = brainmap.split("/");
            image_name = image_name[image_name.length-1]
	    image_names.push(image_name)
        }
     }

    // Add image buttons at the top
    $("#nidm_images").empty()
    for (i=0; i < image_files.length; i++) {
        image_file = image_files[i] 
        image_name = image_names[i]
        // Make the active image selected
        $("#nidm_images").append("<button onclick=viewimage(\""+ image_file +"\") class='btn btn-primary circle' id='" + image_name +"'>IMAGE " + i + "</button>")
    }

    // Load the first map, whatever it is
    file = image_files[0]
    setTimeout(function(){
        viewimage(file)
    },500);
    
}

function view_nidm(nidm_file){

   // Load the table
   nidm_table(peaks[nidm_file])

   // Load the images
   load_images(brain_images[nidm_file])

}
