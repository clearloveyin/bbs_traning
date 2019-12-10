<template>
  <div style="background-color: #EBEBEB;min-height:900px">
    <div style="width:100%;background-color: #636363; overflow: hidden">
            <span class="demonstration" style="float:left;padding-top:10px;color:white;margin-left:1%">
                BBS首页
            </span>
      <!-- <span class="demonstration" style="float:left;padding:5px;color:white;margin-left:2%;width:15%">
                <el-input
                  placeholder="请输入"
                  icon="search"
                  v-model="searchCriteria"
                  :on-icon-click="handleIconClick">
                </el-input>
            </span> -->
      <span class="demonstration" style="float:right;padding-top:10px;margin-right:1%">
                <el-dropdown trigger="click">
                  <span class="el-dropdown-link" style="color:white">
                    {{username}}<i class="el-icon-caret-bottom el-icon--right"></i>
                  </span>
                  <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item @click.native="dialogVisible = true">个人信息</el-dropdown-item>
                    <el-dialog
                      title="个人信息"
                      :visible.sync="dialogVisible"
                      width="30%"
                      :before-close="handleClose"
                      :append-to-body='true'>
                      <el-form ref="form" :model="formUser" label-width="80px">
                          <el-form-item label="用户名">
                          <el-input v-model="formUser.user_name"></el-input>
                          </el-form-item>
                          <el-form-item label="旧密码">
                            <el-input v-model="formUser.old_password" placeholder="必填！"></el-input>
                          </el-form-item>
                          <el-form-item label="新密码">
                            <el-input v-model="formUser.new_password" placeholder="不填代表不更新密码！"></el-input>
                          </el-form-item>
                      </el-form>
                      <span slot="footer" class="dialog-footer">
                          <el-button @click.native="closeDialog">取 消</el-button>
                          <el-button type="primary" @click.native="submitKey">确 定</el-button>
                      </span>
                    </el-dialog>
                    <el-dropdown-item @click.native="loginOut">退出登录</el-dropdown-item>
                  </el-dropdown-menu>
                </el-dropdown>
            </span>
    </div>
    <div style="margin-top:5px">
      <el-row :gutter="10">
        <el-col :xs="4" :sm="4" :md="4" :lg="4">
          <div>
            <el-menu default-active="1" class="el-menu-vertical-demo" style="min-height:900px" @select="handleSelect">
              <el-menu-item index="note"><i class="el-icon-message"></i>帖子</el-menu-item>
              <!-- <el-menu-item index="newNote">最新帖子</el-menu-item>
              <el-menu-item index="topNote">加精帖子</el-menu-item>
              <el-menu-item index="likeNote">点赞最多</el-menu-item>
              <el-menu-item index="issueNote">评论最多</el-menu-item> -->
              <el-menu-item index="model"><i class="el-icon-message"></i>版块</el-menu-item>
              <el-menu-item index="user"><i class="el-icon-message"></i>用户管理</el-menu-item>
              <!-- <el-menu-item v-for="model in models" :index="model.model_id" :key="index">{{model.model_name}}</el-menu-item> -->
            </el-menu>
          </div>
        </el-col>
        <el-col :xs="20" :sm="20" :md="20" :lg="20">
          <div>
            <!-- <div style="border: 1px solid #A6A6A6; border-radius:6px; padding:5px; margin:2px; background-color: white"> -->
              <!-- <el-breadcrumb separator="/"> -->
                <!-- <span class="demonstration" style="float:left;padding-top:10px;color:white;margin-left:1%"> -->
                  <!-- <h1>{{breadcrumbItems}}</h1>> -->
                  
                <!-- </span> -->
                <!-- <el-breadcrumb-item v-for="item in breadcrumbItems" :key="index">{{item}}</el-breadcrumb-item> -->
              <!-- </el-breadcrumb> -->
            <!-- </div> -->
          </div>
 
          <div style="margin-top:10px">
            <router-view></router-view>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>
<Children :name="sonTile"></Children>
<script>
  import axios from 'axios'
  import page5 from '@/components/page5'
  export default {
    components: { page5 },
    data(){
      return{
        dialogVisible: false,
        formUser: {
          user_name: '',
          old_password: '',
          new_password: ''       
        },
        username: '',
        models: [],
        searchCriteria: '',
        breadcrumbItems: '帖子',
        sonTile: '父页面的数据'
       }
     },
     mounted: function() {
        this.initdata()
      },
 
    methods: { //定义函数
      initdata: function() {
       this.username = sessionStorage.getItem('user');
       this.formUser.user_name = sessionStorage.getItem('user');                        
      //   axios.get('/api/model')
      //       .then(response => {
      //         console.log(response.data.content);
      //         this.models = response.data.content;
      //        })
      },           
     //  handleClose(done) {
     //   this.$confirm('确认关闭？')
     //   . then(_ => {
     //   })
     //   .catch(_ => {});
     //   },
        closeDialog: function(){
            this.formUser.user_name = sessionStorage.getItem('user');
            this.dialogVisible = false
        },
        handleClose(done) {
        this.$confirm('确认关闭？')
          .then(_ => {
            done();
          })
          .catch(_ => {});
        },
        submitKey: function() {
           if(this.formUser.user_name != '' && this.formUser.old_password != ''){
             axios.post('/user/update/'+sessionStorage.getItem('user_id'), this.formUser)
                 .then(response => {
                     // post 成功，response.data 为返回的数据
                     if(response.data.result === 'OK'){
                       this.formUser.user_name = sessionStorage.getItem('user');
                       this.$alert('修改成功！')
                       this.dialogVisible = false
                     }else{
                       this.$alert(response.data.error)
                     }
                 })
                 .catch(error => {
                     // 请求失败
                     this.$alert("服务异常！")
                 })
             
           }else{
             this.$alert('用户名和旧密码不能为空！')
         }
       },
       handleSelect(key, keyPath){
         if(key == 'note'){
           this.$router.push({path: '/firstPage', query:{noteType: 'newNote'}});
           this.breadcrumbItems  = '帖子';
         }else if(key == "model"){
           this.$router.push('/page2');
           this.breadcrumbItems  = '版块';
         }else if(key == "user"){
           this.$router.push('/page3');
           this.breadcrumbItems  = '用户管理';
         }else{
           
         }
     }, 
     loginOut:function(){
        sessionStorage.clear();  //清除所有session值
        this.$router.push('/');
     }
               
   }
  }
</script>