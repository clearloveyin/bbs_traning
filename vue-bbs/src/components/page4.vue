<template>
    <div>
        <h1>{{title}}</h1>
        <el-button type="danger" circle @click="noteLike">👍{{like_num}}</el-button>
        <h5>作者：{{create_user}}   时间：{{create_time}}</h5>
        <pre>{{content}}</pre>
        <br>
        <br>
        <ol>
          <li v-for="issue in issue_list">
            <span>{{issue.comment}}</span>
            <br>
            <span>作者：{{issue.create_user}}   时间：{{issue.create_time}}</span>
            <el-divider></el-divider>
          </li>
        </ol>
        <el-input
          type="textarea"
          :rows="2"
          placeholder="请输入评论内容"
          v-model="textarea">
        </el-input>
        <br>
        <br>
        <el-button type="primary" @click="postIssue">提交评论</el-button>
    </div>
  </template>
  <script>
    import axios from 'axios'
    export default {
      data(){
        return {
            note_id: null,
            title: "",
            content: "",
            create_user: "",
            create_time: "",
            issue_list: [],
            textarea: "",
            like_num: 0
        }
      },
      mounted: function() {
        this.note_id= this.$route.query.note_id;
        this.title=this.$route.query.title;
        this.initData();
      },
      methods: { //定义函数
        initData: function(){
            axios.get('/note/info/'+this.note_id)
                .then(response => {
                    if (response.data.result == 'OK'){
                        this.content = response.data.content.content;
                        this.create_user = response.data.content.user_name;
                        this.create_time = response.data.content.create_time;
                        this.issue_list = response.data.content.issue_list;
                        this.like_num = response.data.content.like_num;
                    }else{
                        this.$alert(response.data.error)
                    }
                })
                .catch(error => {
                    // 请求失败
                    this.$alert("服务异常！")
                })

        },
        postIssue: function(){
          if(this.textarea == ""){
            this.$alert('评论内容不能为空！')
          }
          axios.post('/issue/note', {
                  user_id: sessionStorage.getItem('user_id'),
                  note_id: this.note_id,
                  comment: this.textarea
                })
                .then(response => {
                    if (response.data.result == 'OK'){
                        this.textarea = "";
                        location.reload()
                    }else{
                        this.$alert(response.data.error)
                    }
                })
                .catch(error => {
                    // 请求失败
                    this.$alert("服务异常！")
                })
        },
        noteLike: function(){
          axios.get('/note/like/'+this.note_id
                )
                .then(response => {
                    if (response.data.result == 'OK'){
                        this.like_num = response.data.content;
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
