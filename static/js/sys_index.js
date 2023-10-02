
function bindBtnAddEvent(){
    $('#btnAddCust').click(function(){
        console.log('click add cust');
        $('#modalAddCust').modal('show');
    });
}
$('#cust_logo2').filebox({
    onChange: function(e){
        fileUpload(this, 'cust_logo2');
    }
});

function fileUpload(_obj, comp_id){
    console.log('准备上床文件');
    let value = $("#" + comp_id).filebox('getValue');
    let files = $("#" + comp_id).next().find('input[type=file]')[0].files;
    let files2 = $(_obj).context.ownerDocument.activeElement.files;
    console.log(files2);
    if(value && files[0]){
        let formData = new FormData();
        formData.append("folder", '数据导入文件');
        formData.append("guid", 'guid');
        formData.append('file', files[0]);//默认的文件数据名为“Filedata”
        $.ajax({
            url: '/uploader', //单文件上传
            type: 'POST',
            processData: false,
            contentType: false,
            data: formData,
            success: function (res) {
                console.log(res);
                $('#cust_logo').val(res);
            }
        });
    }
}


function initDatagrid(){
    $('#dgCustList').datagrid({
        title: '客户列表',
        toolbar: [{
            iconCls: 'icon-add',
            text: '新增客户',
            handler: function(){openWinAddCust();}
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
        frozenColumns: [[
            {field:'oper',title:'操作',width:'10%',align:'center',
                formatter:function(value, row, index){
                    let btnString = ''
                    btnString += "<a href='javascript:void(0)' style='margin:0px 5px;' onclick='openWinEditCust("+JSON.stringify(row)+");' title='编辑'><i class='fas fa-edit'></i>编辑</a>"
                    btnString += "<a href='javascript:void(0)' style='margin:0px 5px;' onclick='deleteCust("+row.id+");'><i class='fas fa-trash-alt'></i>删除</a>"
                    return btnString;
                }
            },
            {field:'cust_name',title:'客户单位名称',width:'10%',align:'center'}
        ]],
        columns: [[
            {field:'id',title:'ID',width:'10%', hidden:true},
            {field:'cust_addr',title:'客户单位地址',width:'10%',align:'center'},
            {field:'cust_logo',title:'客户单位logo',width:'10%',align:'center',
                formatter: function(value, row, index){
                    return "<img src='"+value+"' style='width:18px;'>"
                }
            },
            {field:'cust_logo2',title:'客户单位logo',width:'10%',align:'center',
                formatter: function(){
                    return "<img src='/static/image/data/client.jpg' style='width:18px;'>"
                }
            },
            {field:'link_name',title:'客户接口人',width:'10%',align:'center'},
            {field:'link_phone',title:'接口人电话',width:'10%',align:'center'},
            {field:'party_name',title:'年会名称',width:'10%',align:'center'},
            {field:'plan_date',title:'年会举办日期',width:'10%',align:'center'},
            {field:'user_num',title:'参会人数',width:'10%',align:'center'},
            {field:'cust_account',title:'客户账号',width:'10%',align:'center'},
            {field:'remark',title:'备注',width:'10%',align:'center'},
            {field:'create_user',title:'添加人',width:'10%',align:'center'},
            {field:'create_time',title:'添加时间',width:'10%',align:'center'}
        ]],
        onLoadSuccess: function (){
        }
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

function openWinAddCust(){
    $('#winAddCust').window({'title': '新增客户信息'});
    $('#winAddCust').window('open');
}

function openWinEditCust(row){
    console.log(row);
    $('#cust_id').val(row.id);
    $('#cust_name').textbox('setValue', row.cust_name);
    $('#cust_addr').textbox('setValue', row.cust_addr);
    $('#cust_logo').textbox('setValue', row.cust_logo);
    $('#link_name').textbox('setValue', row.link_name);
    $('#plan_date').textbox('setValue', row.plan_date);
    $('#winAddCust').window({'title': '编辑客户信息'});
    $('#winAddCust').window('open');
}

function deleteCust(cust_id){
    $.messager.confirm('操作提示', '确定要删除吗?', function(r){
        if (r){
            $.ajax({
            url: "/del_cust_info",
            type: "post",
            data: {'cust_id': cust_id},
            dataType: "JSON",
            success: function(res){
                console.log(res)
                if (res.res_code == '0'){
                    $('#dgCustList').datagrid('load');
                }
            }
        });
        }
    });
}

function closeWinAddCust(){
    $('#cust_id').val('');
    $('#cust_name').textbox('clear');
    $('#cust_addr').textbox('clear');
    $('#cust_logo').val('');
    $('#link_name').textbox('clear');
    $('#plan_date').datebox('clear');
    $('#winAddCust').window('close');
}


function submitWinAddCust(){
    let form_data = $('#formAddCust').serialize();
    let cust_id = $('#cust_id').val();
    console.log(form_data);
    if (!!cust_id){
        $.ajax({
            url: "/edit_cust_info",
            type: "post",
            data: $('#formAddCust').serialize(),
            dataType: "JSON",
            success: function(res){
                console.log(res)
                if (res.res_code == '0'){
                    $('#dgCustList').datagrid('load');
                    closeWinAddCust();
                }
            }
        });
    }else if(!cust_id || cust_id==''){
        $.ajax({
            url: "/add_cust_info",
            type: "post",
            data: $('#formAddCust').serialize(),
            dataType: "JSON",
            success: function(res){
                console.log(res)
                if (res.res_code == '0'){
                    $('#dgCustList').datagrid('load');
                    closeWinAddCust();
                }
            }
        });
    }
}