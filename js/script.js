
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

function load_nidm(nidm_file){

    peak_table = peaks[nidm_file];
    nidm = nidm_file;

    // Add image buttons at the top
    $("#nidm_images").empty()
    for (i=0; i < peak_table.length; i++) {
        image_file = peak_table[i][location_key]
        image_name = peak_table[i][filename_key] 
        image_name = image_names.replace(".nii.gz","").replace(".nii","")
        $("#nidm_images").append('<li><a href="#" onclick=view_nidm(\'' + image_file + '\') id="' + image_name + '" title="' + image_name + '" alt="' + image_name + '">'+ image_name + '</a></li>');
    }
    
    // Set column names specific to nidm file
    columns = column_names[nidm_file]

    // Load the first map, whatever it is
    view_nidm(peak_table[0][location_key])
    
}

function view_nidm(image_filename){

   // Load the table
   nidm_table(image_filename)

   // Update the image
   setTimeout(function(){
        viewimage(image_filename)
   },500);

}
