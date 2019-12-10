<template>
<div>
  <el-table 
    ref="multipleTable"
    :data="tableData"
    tooltip-effect="dark"
    style="width: 100%"
    @selection-change="handleSelectionChange">
    <el-table-column v-for="(item,key) in tableHeader"
                     :key="key"
                     :prop="item.value"
                     :label="item.name"
                     sortable
                     :width="item.width"   
                     :type="item.type"
      >
    </el-table-column>
    
  </el-table>
  <el-pagination
      name="fenye"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page.sync="currentPage"
      :page-sizes="[10, 20, 30]"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total="total">
    </el-pagination>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        tableData: [{
          date: '2016-05-03',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          date: '2016-05-02',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }],
        multipleSelection: [],
        currentPage:1,
        pageSize:10,
        sort:1,
        total:0,
        pageCondition: ''
      }
    },
    props:[
        'tableHeader','searchInfo'
    ],
    methods: {
      toggleSelection(rows) {
        if (rows) {
          rows.forEach(row => {
            this.$refs.multipleTable.toggleRowSelection(row);
          });
        } else {
          this.$refs.multipleTable.clearSelection();
        }
      },
      handleSelectionChange(val) {
        this.multipleSelection = val;
      },
      //修改每页条数触发
      handleSizeChange(val) {
        this.currentPage = 1;
        this.pageSize = val;
        this.tableChang();
      },
      //翻页触发
      handleCurrentChange(val) {
        this.currentPage = val;
        this.tableChang();
      },
      //更新table数据
      tableChang(){
        this.pageCondition = this.searchInfo.data;
        //console.log(this.searchInfo);
        // this.tableData.push( {
        //   date: '2016-05-03',
        //   name: '王小虎',
        //   address: '上海市普陀区金沙江路 1518 弄'
        // });
        this.pageCondition.pageSize = this.pageSizecurrent;
        this.pageCondition.currentPageorderBy = this.currentPageorderBy;
        this.pageCondition.tablePropsort = this.tablePropsort;
        this.pageCondition.sort = this.sort;
        var obj = this ;
        this.$http({
          method:'get',
          url:this.searchInfo.url,
          data:this.pageCondition
        }).then(function(res){
          //console.log(res.data.total);
          //console.log(res.data.list);
          console.log(obj.total);
          obj.total = res.data.total;
          obj.tableData = JSON.parse(JSON.stringify(res.data.list));
          console.log(total);
          //console.log(tableData);
        }).catch(function(err){
          console.log(err)
        })
        // this.$post(this.searchInfo.url,this.pageCondition).then(res=>{
        //   this.total = res.data.total;
        //   this.tableData = JSON.parse(JSON.stringify(res.data.list));
        // })
      }
    }
  }
</script>