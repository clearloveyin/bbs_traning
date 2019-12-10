import Vue from 'vue'
import Router from 'vue-router'
// import HelloWorld from '@/components/HelloWorld'
import login from '@/components/Login'
import demo from '@/components/demo'
import elementUI from '@/components/elementUI'
import table from  '@/components/table'
import table1 from  '@/components/table1'
import firstPage from '@/components/first-page'
import page1 from '@/components/page1'
import page2 from '@/components/page2'
import page3 from '@/components/page3'
import page4 from '@/components/page4'
import page5 from '@/components/page5'
Vue.use(Router)

export default new Router({
  //mode: 'history',
  routes: [
    {
      path: '/',
      name: 'login',
      component: login
    },
    {
      path: '/demo',
      name: 'demo',
      component: demo,
      redirect:"page1",//重定向，第一次进入就进入Page1，不添加的话第一次进入右侧是空白
      children:[
        {
          path: '/page1',
          name: 'page1',
          component: page1
        },
        {
          path: '/page2',
          name: 'page2',
          component: page2
        },
        {
          path: '/page3',
          name: 'page3',
          component: page3
        },
        {
          path: '/page4',
          name: 'page4',
          component: page4
        },
        {
          path: '/firstPage',
          name: 'page5',
          component: page5
        },
      ]
    },
    {
      path: '/elementUI',
      name: 'elementUI',
      component: elementUI
    },
    {
      path: '/table',
      name: 'table',
      component: table
    },
    {
      path: '/table1',
      name: 'table1',
      component: table1
    }
  ]
})
