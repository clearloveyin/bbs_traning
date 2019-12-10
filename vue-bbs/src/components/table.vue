<template>
  <div>
    <el-table
    ref="multipleTable"
    :data="tableData3"
    tooltip-effect="dark"
    style="width: 100%"
    @selection-change="handleSelectionChange">
    <el-table-column
      type="selection"
      width="55">
    </el-table-column>
    <el-table-column
      label="日期"
      width="120">
      <template slot-scope="scope">{{ scope.row.date }}</template>
    </el-table-column>
    <el-table-column
      prop="name"
      label="姓名"
      width="120">
    </el-table-column>
    <el-table-column
      prop="address"
      label="地址"
      show-overflow-tooltip>
    </el-table-column>
  </el-table>
  <div style="margin-top: 20px">
    <el-button @click="toggleSelection([tableData3[1], tableData3[2]])">切换第二、第三行的选中状态</el-button>
    <el-button @click="toggleSelection()">取消选择</el-button>
  </div>
  <sl-table :tableKey="tableKey" :tablep="tablep" ></sl-table>
  <table1 :tableHeader="tableHeader" :searchInfo="searchInfo" ></table1>
  <selector :url="'/option'" :value="svalue" :fileType="{'value':'dasm','label':'dasmb'}"></selector>

  </div>
</template>
<script>
import Table from '../components/tableBox';
import Table1 from '../components/table1';
import selector from '../components/selector';
// v-model="isShow"
  export default {
    components: {'sl-table': Table,'table1': Table1,'selector': selector},
    data() {
      return {
        svalue:'beijing',
        tableData3: [{
          date: '2016-05-03',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }, {
          date: '2016-05-02',
          name: '王小虎',
          address: '上海市普陀区金沙江路 1518 弄'
        }],
        multipleSelection: [],
        tableKey: [
          {
            type:'selection'
          },
          {
          name: '用户名',
          value: 'username',
          width: 20
        },{
          name: '密码',
          value: 'password',
          width: 66
        },{
          name: '昵称',
          value: 'othername',
          width: 66
        }],
        tablep:{
          url:'后台数据接口',
          prop:'排序字段',
          order: 'descending' //descending为倒序aescending为正序
        },
        tableHeader: [
          {
            type:'selection'
          },
          {
          name: '日期',
          value: 'date',
          width: 200
          },
          {
          name: '姓名',
          value: 'name',
          width: 200
          },
          {
          name: '地址',
          value: 'address',
          width: 400
          }],
        searchInfo:{
          url:'/news',
          data: {
            pageSize: '',
            currentPageorderBy: '',
            tablePropsort: '',
            sort: ''
          }
          
        },
      }
    },

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
      }
    }
  }
</script>