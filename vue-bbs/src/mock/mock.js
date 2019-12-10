// 使用 Mock
// var Mock = require('mockjs')
// var data = Mock.mock({
// 	// 属性 list 的值是一个数组，其中含有 1 到 10 个元素
// 	'list|1-10': [{
// 		// 属性 id 是一个自增数，起始值为 1，每次增 1
// 		'id|+1': 1
// 	}]
// })
const Mock = require('mockjs');
// 获取 mock.Random 对象
const Random = Mock.Random;
 // mock一组数据

 const produceData = function (opt) {
  let articles = [];

  for (let i = 0; i < 15; i++) {
   let newArticleObject = {
    name: Random.csentence(0, 3), // Random.csentence( min, max )
    //name: Random.dataImage('300x250', 'mock的图片'), // Random.dataImage( size, text ) 生成一段随机的 Base64 图片编码
    address: Random.cname(), // Random.cname() 随机生成一个常见的中文姓名
    date: Random.date() + ' ' + Random.time() // Random.date()指示生成的日期字符串的格式,默认为yyyy-MM-dd；Random.time() 返回一个随机的时间字符串
   }
   articles.push(newArticleObject)
  }
  return {
   list: articles,
	total: 30
  }
 }

 const dictData = function (opt) {
	let dictData = [{
		value: 'beijing',
		label: '北京市'
	  },
	  {
		value: 'shanghai',
		label: '上海市'
	  },
	  {
		value: 'shenzhen',
		label: '深圳市'
	  }
	]
	return {
		list: dictData
	}
 }
Mock.mock('/news', /post|get/i, produceData);//当post或get请求到/news路由时Mock会拦截请求并返回上面的数据
Mock.mock('/option', /post|get/i, dictData);