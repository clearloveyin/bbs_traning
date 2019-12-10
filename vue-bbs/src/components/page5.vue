<template>
    <div>
        <h1>{{name}}</h1>
        <el-button @click="initData('newNote')" type="text">最新帖子</el-button>
        <el-button @click="initData('topNote')" type="text">加精帖子</el-button>
        <el-button @click="initData('likeNote')" type="text">点赞最多</el-button>
        <el-button @click="initData('issueNote')" type="text">评论最多</el-button>
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
        props:{
            name:{
  		        type: String,
  		        default:''
  	        }
        },
        data(){
        return {
            model_id: null,
            form: {
                note_name: '',
                content: '',
                user_id: null,
                model_id: null
            },
            tableData: [],
            noteType: ''
        }
      },
      mounted: function() {
        this.noteType = this.$route.query.noteType;
        this.initData(this.noteType);
      },
      methods: { //定义函数
        initData: function(noteType){
            axios.get('/note/list/'+noteType)
                .then(response => {
                this.tableData = response.data.content;
                })
                .catch(error => {
                    // 请求失败
                    this.$alert("服务异常！")
                })

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