// Create tables dynamically for nidm results

function nidm_table(data) {
           
    $("#papayaContainer0").css("padding-left","0px")     

    var tablehtml = '<div class="fresh-table full-color-blue"><output id="list"></output><div class="toolbar"><button id="export" class="btn btn-default">Export SVG</button></div><table id="fresh-table" class="table"><thead><th data-field="cluster" data-sortable="true">Cluster</th><th data-field="x" data-sortable="true">X</th><th data-field="y" data-sortable="true">Y</th><th data-field="z" data-sortable="true">Z</th><th data-field="equiv_z" data-sortable="true">Equiv_Z</th><th data-field="pval_fwer" data-sortable="true">pval_fwer</th><th data-field="actions"></th></thead><tbody>'

    // Now add data to the table!
    for(var i=0; i<data.length; i++) {
        result = data[i]           
        var cluster_name = result["wasDerivedFrom"].split("/")
        cluster_name = cluster_name[cluster_name.length-1]   
        tablehtml = tablehtml + '<tr style="background-color:none"><td>' +
                                cluster_name +'</td><td>' + 
                                result["x"] +'</td><td>' + 
                                result["y"] +'</td><td>' + 
                                result["z"] +'</td><td>' + 
                                parseFloat(result["value"]).toFixed(3) + '</td><td>' + 
                                parseFloat(result["pvalue_fwer"]).toFixed(3) + '</td>' + 
                                '<td><button class="btn btn-default circle" style="padding:2px" onclick=move_coordinate(' + 
                                result["x"] + ',' + result["y"] + ',' +
                                result["z"] + ')><i class="fb icon-crosshair"></i></button></td></tr>'
    }  

    tablehtml = tablehtml + '</tbody></table></div>'

    $("#tablerow").empty()
    $("#tablerow").append($(tablehtml))

    var $table = $('#fresh-table'),
    $exportBtn = $('#export'), 
    full_screen = false,
    window_height;
 
    window_height = $(window).height();
    table_height = window_height - 20;
                   
    $table.bootstrapTable({
        toolbar: ".toolbar",
        showRefresh: false,
        search: true,
        showToggle: false,
        showColumns: false,
        pagination: true,
        striped: true,
        sortable: true,
        height: table_height,
        pageSize: 25,
        pageList: [25,50,100],
                
        formatShowingRows: function(pageFrom, pageTo, totalRows){
             //do nothing here, we don't want to show the text "showing x of y from..." 
        },
        formatRecordsPerPage: function(pageNumber){
            return pageNumber + " rows visible";
        },
        icons: {
            refresh: 'fa fa-refresh',
            toggle: 'fa fa-th-list',
            columns: 'fa fa-columns',
            detailOpen: 'fa fa-plus-circle',
            detailClose: 'fa fa-minus-circle'
         }
    });
            
    window.operateEvents = {
        //'click .like': function (e, value, row, index) {
        //    alert('You click like icon, row: ' + JSON.stringify(row));
        //    console.log(value, row, index);
        //},
        //'click .edit': function (e, value, row, index) {
        //    alert('You click edit icon, row: ' + JSON.stringify(row));
        //    console.log(value, row, index);    
        //},
        'click .remove': function (e, value, row, index) {
        $table.bootstrapTable('remove', {
            field: 'id',
            values: [row.id]
            });   
           }
        };
            
        $exportBtn.attr("onclick","export_svg()")
            
        $(window).resize(function () {
           $table.bootstrapTable('resetView');
        });    
 
}
