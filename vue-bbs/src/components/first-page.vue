<template>
<div id="app">
  <el-container class="con_section">
    <el-header class="blueheader">
      <h2 class="headlogo">Python论坛</h2>
      <el-col :span="3">
        <el-button type="text" @click="dialogVisible = true">添加版块</el-button>

        <el-dialog
          title="添加版块"
          :visible.sync="dialogVisible"
          width="30%"
          :before-close="handleClose">
          <el-form ref="form" :model="form" label-width="80px">
            <el-form-item label="版块主题">
              <el-input v-model="formData.modelName"></el-input>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button @click="dialogVisible = false">取 消</el-button>
            <el-button type="primary" @click.native="submitKey">确 定</el-button>
          </span>
        </el-dialog>
      </el-col>
      <el-col :span="3" class="userinfo">
        <span>{{username}}</span>
      </el-col>
    </el-header>
    <el-container>
      <el-aside style="flex: 0 0 230px;width: 230px;background:#eef1f6">
        <el-menu default-active="1" class="el-menu-vertical-demo" @select="handleSelect">
            <el-menu-item :index="i" :key="index">
              <span>版块</span></el-menu-item>
            <el-menu-item v-for="model in models" :index="model.model_id" :key="index">
              <span>{{model.model_name}}</span></el-menu-item>
        </el-menu>
      </el-aside>
      <el-main class="home_main">
        <div>
          <div style="border: 1px solid #A6A6A6; border-radius:6px; padding:5px; margin:2px; background-color: white">
            <el-breadcrumb separator="/">
              <el-breadcrumb-item v-for="item in breadcrumbItems" :key='index'>{{item}}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
        </div>
      </el-main>
    </el-container>
  </el-container>
</div>
</template>

<script>
  import axios from 'axios'
  export default {
       data(){
         return{
          dialogVisible: false,
          formData: {
            modelName: '',
            userId: 0         
          },
          username: '',
          models: [],
          searchCriteria: '',
          breadcrumbItems: ['版块'],
         }
       },
       mounted: function() {
          this.initdata()
        },
       methods: { //定义函数
       			initdata: function() {
              this.username = sessionStorage.getItem('user');                        
       				axios.get('/api/model')
       				    .then(response => {
       				      console.log(response.data.content);
       				      this.models = response.data.content;
       				     })
       				},           
            //  handleClose(done) {
            //   this.$confirm('确认关闭？')
            //   . then(_ => {
            //   })
            //   .catch(_ => {});
            //   },
              submitKey: function() {
                  this.formData.userId = sessionStorage.getItem('user_id');
                  if(this.formData.modelName !== ''){
                    axios.post('/api/model', this.formData)
                        .then(response => {
                            // post 成功，response.data 为返回的数据
                            if(response.data.result === 'OK'){
                              this.$alert('添加成功！')
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
              handleIconClick(ev) {
                console.log(ev);
              },
 
              handleSelect(key, keyPath){
                if(key === null){
                  this.$router.push('/page1');
                  this.breadcrumbItems  = ['page1'];
                }else{
                  this.$router.push('/page2');
                  this.breadcrumbItems  = ['page2'];
                }
            },                
          }
        }          
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .con_section{
    position: absolute;
    top: 0px;
    bottom: 0px;
    left:0px;
    width:100%;
  }
  .blueheader {
    height: 60px;
    line-height: 60px;
    background: #67c23a;
    color: #fff;
  }
  .el-menu-item.is-active {
      color: #67c23a;
  }
  .headlogo{
    float: left;
    height: 60px;
    margin: 0 20px;
    width: 300px;
  }
  ul.el-menu {
    background: #e4e8f1;
  }
  .userinfo{
    position: absolute;
    right: 0;
  }
  .el-submenu__title{
    background:#eef1f6;
  }
  .el_main{
    padding:0px;
  }
  .home_main{
    padding:10px;
  }
  .breadcrumb-container .title {
      width: 200px;
      float: left;
      color: #475669;
    font-size: 13px;
    }
  .breadcrumb-inner {
      float: right;
      font-size: 13px;
  }
  .el-breadcrumb__inner, .el-breadcrumb__inner a {
    font-weight: 400;
  }
</style>
