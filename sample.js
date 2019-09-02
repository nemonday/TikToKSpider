
var mysql  = require('mysql');  

var connection = mysql.createConnection({     
  host     : 'localhost',       
  user     : 'root',              
  password : 'pythonman',       
  port: '3306',                   
  database: 'Tiktok' 
}); 

connection.connect();
connection.timeout = 0;



module.exports = {
  // 模块介绍
  summary: 'my customized rule for AnyProxy',
  // 发送请求前拦截处理
  *beforeSendRequest(requestDetail) {
    const url = requestDetail.url;
      if (requestDetail.url.indexOf('post/?') > 0) {
      var data = requestDetail.requestOptions;
      var path = data['path']

      var str = path;   
      var res = str.match(/user_id=(\d+)/); //没有使用g选项   
      var id = parseInt(res[1])

      var user_url = 'https://'+ data['hostname'] + path
      var headers = data['headers']
      var Host = headers['Host']
      var Connection = headers['Connection']
      var x_Tt_Token = headers['x-Tt-Token']
      var x_tt_trace_id = headers['x-tt-trace-id']
      var Accept_Encoding = headers['Accept-Encoding']
      var Cookie = headers['Cookie']
      var X_Khronos = headers['X-Khronos']
      var X_Gorgon = headers['X-Gorgon'] 

      var  addSql = 'REPLACE INTO work(id, url, Host, Connection, x_Tt_Token, x_tt_trace_id, Accept_Encoding, Cookie, X_Khronos, X_Gorgon) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)';
      var  addSqlParams = [id, user_url, Host, Connection, x_Tt_Token, x_tt_trace_id, Accept_Encoding, Cookie, X_Khronos, X_Gorgon];


      console.log('------------------------------------------------------------------')
      
      console.log(id)
      console.log(typeof id); //boolean

      connection.query('select id from work where id=?', [id], (err, results, fields) => {
          if (err) {
            return console.error(err.message);
          }
          // get inserted id
          if (results == '') {
              connection.query(addSql, addSqlParams, (err, results, fields) => {
                if (err) {
                  return console.error(err.message);
                }
                // get inserted id
                console.log('Todo Id:' + results.insertId);
            });
          } 

        });

      
      console.log('------------------------------------------------------------------')

    }}, 




  *beforeSendResponse(requestDetail, responseDetail) { /* ... */ 
      if (requestDetail.url.indexOf('post/?') > 0) {

      console.log('------1111---------1111--------111----')
      var resdata = responseDetail.response['body'];
      var buf = new Buffer(resdata);
      // console.log(buf.toString('utf8'));


      // console.log(JSON.stringify(resdata))
      console.log('------1111---------1111--------111----')
      }

      
  },

  // 请求出错的事件
  *onError(requestDetail, error) { /* ... */ },
  // https连接服务器出错
  *onConnectError(requestDetail, error) { /* ... */ }
};
  