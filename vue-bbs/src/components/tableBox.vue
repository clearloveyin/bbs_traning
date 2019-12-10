<template>
  <div>
  <el-table :data="tableData"
            :default-sort="{prop:tableProp , order: tableOrder}"
            @sort-change="changes"
            border>
    <el-table-column v-for="(item,key) in tableKey"
                     :key="key"
                     :prop="item.value"
                     :label="item.name"
                     sortable ></el-table-column>
  </el-table>
    <el-pagination
      name="fenye"
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page.sync="currentPage"
      :page-sizes="[10, 15, 20]"
      :page-size="pageSize"
      layout="total, sizes, prev, pager, next, jumper"
      :total=total>
    </el-pagination>
  </div>
</template>
<script>
  export default{
    name: 'mytable',
    data(){
      return{
        tableData: [{
          date: '2016-05-03',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          date: '2016-05-02',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }],
        currentPage:1,
        pageSize:10,
        tableProp:this.tablep.prop,
        tableOrder:this.tablep.order,
        sort:1,
        total:0
      }
    },
    props:['tableKey','tablep'],
    methods:{
    //table排序触发
      changes({ column, prop, order }){
        this.tableProp = prop;
        this.tableOrder = order;
        if(order !== 'descending'){
            this.sort = 0;
        }else{
            this.sort = 1;
        }
        this.tableChang();
        return false;
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
        this.$post(this.tablep.url,{
          pageSize: this.pageSize,
          current: this.currentPage,
          orderBy:this.tableProp,
          sort:this.sort
        }).then(res=>{
          this.total = res.data.total;
          this.tableData = JSON.parse(JSON.stringify(res.data.list));
        })
      }
    }
  }
</script>