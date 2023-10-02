
function bindBtnAddEvent(){
    $('#btnAddCust').click(function(){
        console.log('click add cust');
        $('#modalAddCust').modal('show');
    });
}

function initDatagrid(){
    $('#dgCustList').datagrid({
        title: '客户列表',
        toolbar: [{
            iconCls: 'icon-add',
            text: '新增客户',
            handler: function(){alert('add')}
        },'-',{
            iconCls: 'icon-help',
            handler: function(){alert('help')}
        }],
        singleSelect:true,
        rownumbers: true,
        url:'/get_cust_list',
        method:'get',
        pagination:true,
        pageSize: 10,
        pageList: [10,20,30,40,50],
        columns: [[
            {field:'id',title:'ID',width:'10%', hidden:true},
            {field:'cust_name',title:'客户单位名称',width:'10%',align:'center'},
            {field:'cust_addr',title:'客户单位地址',width:'10%',align:'center'},
            {field:'cust_logo',title:'客户单位logo',width:'10%',align:'center'},
            {field:'link_name',title:'客户接口人',width:'10%',align:'center'},
            {field:'link_phone',title:'接口人电话',width:'10%',align:'center'},
            {field:'party_name',title:'年会名称',width:'10%',align:'center'},
            {field:'plan_date',title:'年会举办日期',width:'10%',align:'center'},
            {field:'oper',title:'操作',width:'10%',align:'center'}
        ]]
    });
}

function submitAddCust(){
    $.ajax({
        url: "/add_cust_info",
        type: "post",
        data: $('#formAddCust').serialize(),
        dataType: "JSON",
        success: function(res){
            console.log(res)
            if (res.res_code == '0'){
                //$('#modalAddCust').modal('show');
                $('#modalAddCust').modal('hide');
            }
        }
    });
}


function closeModalAddCust(){
    $('#modalAddCust').modal('hide');
}
