(function ($) {
    $(document).ready(function(){
        var switchid = JSON.parse($("#switch").data("switchid"));
        var switchip = JSON.parse(JSON.stringify($("#switch").data("switchip")));

        $('#switchdata').DataTable({
            responsive: false,
            'ajax': '/switches/' + switchid + '/getswitchdata',
            'columnDefs': [
                {
                    targets: 0,
                    searchable: false,
                    orderable: false,
                    visible: false
                },
                {
                    targets: 1,
                    className: 'dt-body-center'
                },
                {
                    'targets': 4,
                    'render': function (data, type, full, meta) {
                        return '<a class="action" href="' + 'http://' + data + '" target="_blank">' + data + '</a>'; 
                    }
                }
            ],
            order: [1, 'asc'],
            'paging': false,
            scrollX: true,
            'language': {
                'search': '',
                'searchPlaceholder': 'Enter search term'
              },
            'dom': 'Bft<"footer-wrapper"l<"paging-info"ip>>',
            buttons: {
                buttons: [
                    {
                        extend: 'excelHtml5',                        
                        title: null,
                        header: true,
                        filename: switchip.toString(),
                        autoFilter: true,
                        sheetName: switchip.toString()
                    },
                    {
                        extend: 'csvHtml5',
                        fieldBoundary: '',
                        fieldSeparator: ';',
                        filename: switchip.toString(),
    
                        header: false
                    }
                ],
                dom: {
                    button: {
                        className: 'waves-effect waves-light btn'
                    }
                }
            },            
            'drawCallback': function( settings ) {
                var api = this.api();      
                // Add waves to pagination buttons
                $(api.table().container()).find('.paginate_button').addClass('waves-effect');                
                api.table().columns.adjust();
              }
          });

    });
  }( jQuery ));
  