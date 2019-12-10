/* 用户登录 */
import axios from 'axios'

export function myLogin (params) {
  return axios.post('/login', params)('/api/idcs/')
  return request({
    method: 'post',
    url: '/login',
    data: params    //post用data,get用params
  })
}

// export function get_data(pro_id){
// 	return request({
// 	    url: '/GetBaseQuotationList/' + pro_id,
// 	    method: 'get',
// 	})
// }
