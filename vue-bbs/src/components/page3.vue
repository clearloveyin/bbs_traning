<template>
    <div>
            <h1>用户管理</h1>
            <el-row>
                    <el-table
                            :data="tableData"
                            style="width: 100%">
                            <el-table-column
                            prop="user_name"
                            label="用户名"
                            width="400">
                            </el-table-column>
                            <el-table-column
                            prop="role_names"
                            label="角色"
                            width="400">
                            </el-table-column>
                            <el-table-column
                            label="操作">
                            <template slot-scope="scope">
                                <el-button type="text" size='small' @click="openDialog(scope.row)">角色分配</el-button>
                                    <el-dialog
                                      title="角色分配"
                                      :visible.sync="dialogVisible"
                                      width="30%"
                                      :before-close="handleClose">
                                      <el-checkbox v-model="admin">admin(管理员)</el-checkbox>
                                      <el-checkbox v-model="moderator">moderator(版主)</el-checkbox>
                                      <span slot="footer" class="dialog-footer">
                                          <el-button @click="closeDialog">取 消</el-button>
                                          <el-button type="primary" @click="postUserRole()">确 定</el-button>
                                      </span>
                                    </el-dialog>
                                <el-button @click="deleteUser(scope.row.user_id)" type="text" size="small">删除</el-button>
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
            tableData: [],
            admin: false,
            moderator: false,
            row_user_id: null
        }
      },
      mounted: function() {
        this.initdata()
      },
      methods: { //定义函数
        initdata: function() {   
            // this.$alert("----")                 
            axios.get('/user/list/'+sessionStorage.getItem('user_id'))
                .then(response => {
                    if(response.data.result === 'OK'){
                        this.tableData = response.data.content;
                    }else{
                        this.$alert(response.data.error)
                    }
                
                })
                .catch(error => {
                    // 请求失败
                    this.$alert("服务异常！")
                })
            }, 
        closeDialog: function(){
            this.admin = false;
            this.moderator = false;
            this.dialogVisible = false;
        },
        openDialog: function(row){
            this.row_user_id = row.user_id;
            var roles = row.role_names;
            if (roles != ''){
                if(roles.indexOf('admin') != -1){
                    this.admin = true
                }
                if(roles.indexOf('moderator') != -1){
                    this.moderator = true
                }
            }
            this.dialogVisible = true;
        },
        postUserRole: function(){
            
            axios.post('/user/role',
                { 
                        user_id: this.row_user_id,
                        admin: this.admin,
                        moderator: this.moderator, 
                }
            )
            .then(res =>{
                if(res.data.result === 'OK'){
                    this.$alert('保存成功');
                    this.row_user_id = null;
                    this.admin = false;
                    this.moderator = false;
                    this.dialogVisible = false;
                    location.reload();
                }else{
                    this.$alert(res.data.error)
                }
            })
            .catch(ferror => {
                this.$alert('服务异常！')
            });
        },
        deleteUser: function(user_id){
            axios.delete('/user',
                {
                    data: { 
                        user_id: user_id
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
        }
                
    }
    }
  </script>