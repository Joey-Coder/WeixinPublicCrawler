## 微信公众号爬虫（搜狗端）  
### 介绍   
* scrapy框架爬取，selenium用于处理验证码以及登陆。    
* 支持爬取公众号主体以及相关文章。    
* 只需登陆一次，自动存储用户凭证。   
* 可接入代理池，自由切换代理。   
* 遇到验证码反爬，可截取验证码图片，等待用户输入正确验证码。    

### 使用   
1. 设置setting中的最大爬取页数MAX_PAGE。   
2. 启动命令：```scrapy crawl sogou_weixin``
3. 根据提示输入想爬取的关键字，例如：吉他     

### 其他
* 如果想以表格形式导出爬取内容：
```bash
    scrapy crawl sogou_weixin -o xxxx.csv
```    
* 如果想接入proxy池，先在setting中设置PROXY_URL。然后取消middleware.py中proxy中间件的注释。    

### 待办    
* 接入第三方打码平台  ...... [ ]