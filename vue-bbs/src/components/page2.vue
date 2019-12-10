<template>
    <div>
        <h1>版块管理</h1>
        <el-row>
            <el-button type="primary" @click="dialogVisible = true">添加版块</el-button>
            <br><br>
            <el-dialog
                title="添加版块"
                :visible.sync="dialogVisible"
                width="30%"
                :before-close="handleClose">
                <el-form ref="form" :model="formData" label-width="80px">
                    <el-form-item label="版块主题">
                    <el-input v-model="formData.modelName"></el-input>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                    <el-button @click.native="closeDialog">取 消</el-button>
                    <el-button type="primary" @click.native="submitKey">确 定</el-button>
                </span>
            </el-dialog>
        </el-row>
            <span></span>
        <el-row>
        <el-table
                :data="tableData"
                style="width: 100%">
                <el-table-column
                prop="model_name"
                label="版块名"
                width="400">
                </el-table-column>
                <el-table-column
                prop="create_time"
                label="创建日期"
                width="400">
                </el-table-column>
                <el-table-column
                label="操作">
                <template slot-scope="scope">
                    <el-button @click="pageRoute(scope.row)" type="text" size="small">查看</el-button>
                    <el-button @click="handleClick(scope.row)" type="text" size="small">删除</el-button>
                </template>
                </el-table-column>
        </el-table>
        </el-row>
    </div>
  </template>
  <script>
    import axios from 'axios'
    export default {
      data(){
        return {
            dialogVisible: false,
            formData: {
                modelName: '',
                userId: 0         
          },
          tableData: []
        }
      },
      mounted: function() {
        this.initdata()
      },
      methods: { //定义函数
        initdata: function() {
            this.username = sessionStorage.getItem('user');                        
            axios.get('/model')
                .then(response => {
                this.tableData = response.data.content;
                })
                .catch(error => {
                    // 请求失败
                    this.$alert("服务异常！")
                })
            },     
        submitKey: function() {
                  this.formData.userId = sessionStorage.getItem('user_id');
                  if(this.formData.modelName !== ''){
                    axios.post('/model', this.formData)
                        .then(response => {
                            // post 成功，response.data 为返回的数据
                            if(response.data.result === 'OK'){
                              this.$alert('添加成功！');
                              this.dialogVisible = false;
                              location.reload();
                            }else{
                              this.$alert(response.data.error)
                            }
                        })
                        .catch(error => {
                            // 请求失败
                            this.$alert("服务异常！")
                        })
                    
                  }else{
                    this.$alert('版块主题不能为空！')
                }
              },
        closeDialog: function(){
            this.dialogVisible = false
        },
        handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
          .catch(_ => {});
        },
        handleClick(row){
            axios.delete('/model/del',
                {
                    data: { 
                    model_id: row.model_id,
                    user_id: sessionStorage.getItem('user_id'), 
                    }
                }
            )
            .then(res =>{
                if(res.data.result === 'OK'){
                    this.$alert('删除成功！');
                    location.reload();
                }else{
                    this.$alert(res.data.error)
                }
            })
            .catch(ferror => {
                this.$alert('服务异常！')
            });
        },
        pageRoute: function(row){
            this.$router.push({
                path: '/page1',
                query: {
                    model_id: row.model_id,
                    title: row.model_name
                }
            })

        }
      }
    }
  </script>