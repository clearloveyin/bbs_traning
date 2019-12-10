<template>
  <div>
    <el-select v-model="svalue" placeholder="请选择" filterable>
      <el-option
        v-for="item in options"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select>
    <!-- <el-button @click="clickme()">默认按钮</el-button> -->
    <!-- <input type="text" :value="value"> -->
  </div>
</template>

<script>
  export default {
    name: 'selector',
    data() {
      return {
        options:[],
        svalue: ''
      }
    },
    methods: {
        // clickme(){
        //     alert(this.svalue);
        // },
        //转换下拉框下的字段
       _dataTransform(data){
          let _data = [];
          for (let i = 0; i < data.length; i++) {
              _data[i] = {};
              _data[i].label = data[i][this.fileType.label];
              _data[i].value = data[i][this.fileType.value];
            }
            return _data;
       }
     },
    //  watch:{
    //     //判断下拉框的值是否有改变
    //     svalue(val, oldVal) {
    //         // console.log('new: %s, old: %s', val, oldVal)
    //         if(val!=oldVal){
    //             console.log(this.svalue);
    //             this.$emit('input', this.svalue); 
    //         }
    //     }, 
    // },
    props: {
       url:{
          type:String
       },//导入的url地址
       value: {
         default:'',
          type:String
       },//接受外部v-model传入的值
       fileType:{
          type:Object
       }//定义请求回来的json数据格式
    },
    mounted(){
        //初始话下拉框的值
        this.svalue=this.value;
        console.log("svalue:" + this.svalue);
        var obj = this;
        //远程请求回来的数据
        this.$http({
          method:'get',
          url:this.url,
        }).then(function(res){
          //console.log(res.data.total);
          //console.log(res.data.list);
          console.log(res);
          obj.options=res.data.list;//obj._dataTransform(res.data.list);
        }).catch(function(err){
          console.log(err)
        })

        // this.$fetch(this.url)
        //     .then((response) => {
        //         this.options=this._dataTransform(response);
        // })
    }
  }
</script>
