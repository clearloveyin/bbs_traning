<template>
    <div>
        <h1>{{title}}</h1>
        <el-button type="primary" @click="dialogFormVisible = true">发布帖子</el-button>
        <br><br>
        <el-dialog title="发布帖子" :visible.sync="dialogFormVisible">
                <el-form :model="form">
                  <el-form-item label="帖子标题" :label-width="formLabelWidth">
                    <el-input v-model="form.note_name" autocomplete="off"></el-input>
                  </el-form-item>
                  <el-form-item label="帖子内容" :label-width="formLabelWidth">
                    <el-input
                        type="textarea"
                        :rows="3"
                        placeholder="请输入内容"
                        v-model="form.content">
                    </el-input>
                  </el-form-item>
                </el-form>
                <div slot="footer" class="dialog-footer">
                  <el-button @click="closeDialog">取 消</el-button>
                  <el-button type="primary" @click="postNote">确 定</el-button>
                </div>
        </el-dialog>
        <el-table
                :data="tableData"
                style="width: 100%">
                <el-table-column
                prop="note_name"
                label="标题"
                width="200">
                </el-table-column>
                <el-table-column
                prop="create_user"
                label="作者"
                width="100">
                </el-table-column>
                <el-table-column
                prop="create_time"
                label="创建时间"
                width="200">
                </el-table-column>
                <el-table-column
                prop="top"
                label="精品贴"
                width="100">
                </el-table-column>
                <el-table-column
                prop="like_num"
                label="点赞数"
                width="100">
                </el-table-column>
                <el-table-column
                prop="issue_num"
                label="评论数"
                width="100">
                </el-table-column>
                <el-table-column
                label="操作">
                <template slot-scope="scope">
                    <el-button @click="pageRoute(scope.row)" type="text" size="small">查看</el-button>
                    <el-button @click="topNote(scope.row.note_id, scope.row.top)" type="text" size="small"
                    v-if="scope.row.top=='普通贴'">加精置顶</el-button>
                    <el-button @click="topNote(scope.row.note_id, scope.row.top)" type="text" size="small"
                    v-else>取消置顶</el-button>
                    <el-button @click="delNote(scope.row.note_id)" type="text" size="small">删除</el-button>
                </template>
                </el-table-column>
        </el-table>
    </div>
  </template>
  <script>
    import axios from 'axios'
    export default {
      data(){
        return {
            model_id: null,
            title: "",
            dialogFormVisible: false,
            form: {
                note_name: '',
                content: '',
                user_id: null,
                model_id: null
            },
            tableData: []
        }
      },
      mounted: function() {
        this.model_id= this.$route.query.model_id;
        this.title=this.$route.query.title;
        this.initData();
      },
      methods: { //定义函数
        initData: function(){
            axios.get('/note/list/'+this.model_id)
                .then(response => {
                this.tableData = response.data.content;
                })
                .catch(error => {
                    // 请求失败
                    this.$alert("服务异常！")
                })

        },
        closeDialog: function(){
                this.form.note_name = '';
                this.form.content = '';
                this.dialogFormVisible = false;
            },
        postNote: function(){
                this.form.user_id = sessionStorage.getItem('user_id');
                this.form.model_id = this.model_id;
                if(this.form.note_name !== ''){
                axios.post('/note/post', this.form)
                    .then(response => {
                        // post 成功，response.data 为返回的数据
                        if(response.data.result === 'OK'){
                            this.$alert('添加成功！');
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
                this.$alert('帖子标题不能为空！')
                }
        },
        pageRoute: function(row){
            console.log(row)
            this.$router.push({
                path: '/page4',
                query: {
                    note_id: row.note_id,
                    title: row.note_name
                }
            })

        },
        topNote: function(note_id, top){
            if(top == '普通贴'){
                var status = true
            }else{
                var status = false
            }
            axios.post('/note/put', {
                        user_id: sessionStorage.getItem('user_id'),
                        model_id: this.model_id,
                        note_id: note_id,
                        status: status
                    })
                    .then(response => {
                        // post 成功，response.data 为返回的数据
                        if(response.data.result === 'OK'){
                            location.reload();
                        }else{
                            this.$alert(response.data.error)
                        }
                    })
                    .catch(error => {
                        // 请求失败
                        this.$alert("服务异常！")
                    })
        },
        delNote: function(note_id){
            axios.delete('/note/put', {
                        data:{
                            user_id: sessionStorage.getItem('user_id'),
                            model_id: this.model_id,
                            note_id: note_id
                        }
                    })
                    .then(response => {
                        // post 成功，response.data 为返回的数据
                        if(response.data.result === 'OK'){
                            location.reload();
                        }else{
                            this.$alert(response.data.error)
                        }
                    })
                    .catch(error => {
                        // 请求失败
                        this.$alert("服务异常！")
                    })
        }
    }
        
    }
  </script>