# SinaSpider
> 爬取新浪新闻信息
> 使用selenium，涉及到模拟登陆，xpath,css元素拾取,翻页，展开全文等
> 将结果保存获取到的数据到json文件，并转化为更加方便宜读写的jsonlines文件

## 获取浏览器驱动
> 两种常用方式，[FireFoxdriver](https://github.com/mozilla/geckodriver/releases)与[chromedriver](http://npm.taobao.org/mirrors/chromedriver/)。


## 模拟登陆，并保存登录信息的cookies到本地，方便下次登录直接读取
>``` login() ```



## 读取含有登录信息的本地cookies，并加入到session当中
> ``` get_cookies() ```



## 搜素新闻内容，并保存
> ``` search_content(content, total_page) ```


## 展开全文
> ``` open_all_text(driver, selector) ```

## json转为jsonlines
> ``` json_to_jsonl(input_path, output_path) ```
