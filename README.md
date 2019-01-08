# Lagou-data-analysis
爬取全国范围的Python岗位信息&amp;画图分析数据
### 数据爬取
##### 爬取内容
全国范围的Python岗位信息
* 请求数据的API是 `https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false`
* `Headers` 中 `Query String Parameters` 是在URL中可见的参数， `Form Data` 是 POST 的数据
* `Preview` 中 `content\positionResult\result`，返回的是查询结果
* 模拟 POST 数据的时候，Headers 中必须带上 `Referer` 和 `User-Agent` 参数

> `Referer` 优点 
> * Http协议头中的 `Referer` 主要用来让服务器判断来源页面，即用户是从哪个页面来的，通常被网站用来统计用户来源，是从搜索页面来的，还是从其他网站链接过来，或是从书签等访问，以便网站合理定位
> * `Referer` 有时也被用作防盗链, 即下载时判断来源地址是不是在网站域名之内, 否则就不能下载或显示

> `Referer` 缺点
> * `Referer` 是不安全的，客户端可以通过设置改变 Request中的值，尽量不要用来进行安全验证等方面

> 为什么要设置 `User-Agent` ?
> * 为了能正常运行，需要隐藏自己爬虫程序的身份，就可以通过设置 `User Agent`（用户代理）的来达到隐藏身份的目的
> * `User Agent` 存放于Headers中，服务器就是通过查看Headers中的 `User Agent` 来判断是谁在访问
> * Python允许修改 `User Agent` 来模拟浏览器访问


##### 反爬虫
* 使用代理IP
```
proxies = {'http': 'http://118.190.95.43:9001', 'http': 'http://61.177.47.86:60086',
               'http': 'http://120.92.74.237:3128'}
               
response = requests.post(proxies=proxies, ... , ...)
```
* 随机选择 `User-Agent` 中的浏览器
```
agents = [
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)'
    ...
    ... 
    ]
    
headers['User-Agent'] = agents.pop(random.randint(0, 6))
```
        
* 爬取每条数据时，设置间隔时间
```
time.sleep(round(random.uniform(3, 5), 2))

time.sleep(random.randint(3, 5))
```

### 存入数据库

### 数据分析
##### 准备
Best way to Install：`pip3 install pandas`
```
import pandas as pd
import matplotlib.pyplot as plt
```

###### [pandas基本语法](https://github.com/yingl/pydata-book/tree/master/ch05_pandas%E5%85%A5%E9%97%A8)
> 两种常见的数据结构：`Series` (一维的标签化数组对象) 和 `DataFrame` (面向列的二维表结构)

###### [matplotlib基本用法](https://www.cnblogs.com/linu/articles/9191564.html)
###### 解决 matplotlib 字体不支持中文
* `/Users/xxx/python/project/venv/lib/python3.7/site-packages/matplotlib/mpl-data/fonts/ttf` 目录下添加 `simhei.ttf`
* 新安装的字体需要更新字体列表缓存，所以把新安装的字体复制到该目录下
* 删除 tex.cache，matplotlib 下次启动时会重建缓存，新字体被添加
```
wenjiadeMacBook-Pro:.matplotlib wenjiasun$ rm -r tex.cache/
```
* 程序开头添加
```
plt.rcParams['font.sans-serif'] = ['simhei']

# 用来正常显示负号
# plt.rcParams['axes.unicode_minus'] = False
```
###### 连接数据库
```
import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', password='xxx', db='lagou_db',
                       charset='utf8', use_unicode=True)
```

##### 城市岗位分布 柱状图
```
# city_datas数据类型：pandas.core.frame.DataFrame
city_datas = pd.read_sql("select city, count(city) as num from lagou_table group by city", conn)
city_datas_index = city_datas.set_index("city")
city_datas_index.sort_values(by="num")[:].num.plot(color='g', kind='bar')
plt.title('City Distribution for Python')
plt.savefig('analysisPis/cityDistribution.png')
plt.show()
```

##### 工作经验 饼图
```
# mysql筛选出某列中的重复值并统计对应数量
experience = pd.read_sql("select work_year,count(work_year) as num from lagou_table group by work_year having count(work_year) > 1", conn)
# 获取DataFrame格式中某列的值
work_year = experience.iloc[:, 0]
num = experience.iloc[:, 1]
# numpy.ndarray类型
work_year_array = work_year.values
num_array = num.values

# 将numpy.ndarray类型转换为list类型
work_year_array = work_year_array.tolist()
num_array = num_array.tolist()

# explode指定饼图某些部分的突出显示，即呈现爆炸式
explode = [0.1, 0, 0.1, 0.1, 0, 0, 0]

plt.pie(num_array, labels=work_year_array, autopct='%1.2f%%', explode=explode)
plt.title('Working Experience Chart')

# supported formats: eps, pdf, pgf, png, ps, raw, rgba, svg, svgz
plt.savefig('analysisPis/experienceChart.png')

plt.show()
```

> [`matplotlib.pyplot.pie()`](https://www.sohu.com/a/199233196_163476)函数：
```
pie(x, explode=None, labels=None, colors=('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w'), autopct=None, pctdistance=0.6, shadow=False, labeldistance=1.1, startangle=None, radius=None, counterclock=True, wedgeprops=None, textprops=None, center = (0, 0), frame = False)
```
> * x：指定绘图的数据，如果sum(x) > 1，会使用sum(x)归一化
> * explode：每一块离开圆心的距离
> * labels：为每一块饼图添加标签说明
> * autopct：控制饼图内百分比设置，可以采用格式化的方法显示，例如 '%1.1f' 指小数点前后位数(没有用空格补齐)

`plt.savefig()` 需要在 `plt.show()` 前调用
> 因为在 `plt.show()` 后实际上已经创建了一个新的空白的图片，这时候使用 `plt.savefig()` 就会保存这个新生成的空白图片

##### 公司规模 饼图
```
size = pd.read_sql("select company_size,count(company_size) as num from lagou_table where company_size not like 'None' group by company_size having count(company_size) > 1", conn)

company_size = size.iloc[:, 0]
num = size.iloc[:, 1]
company_size_array = company_size.values
num_array = num.values

company_size_array = company_size_array.tolist()
num_array = num_array.tolist()
explode = [0.1, 0, 0.1, 0.1, 0, 0]

plt.pie(num_array, labels=company_size_array, autopct='%1.2f%%', explode=explode)
plt.title('Company Size Chart')

plt.savefig('analysisPis/companySize.png')
plt.show()
```

##### 不同城市的平均薪资状况 条形图
```
citys = pd.read_sql("select city, count(city) from lagou_table group by city having count(city) > 1", conn)
city = citys.iloc[:, 0]
city_count = citys.iloc[:, 1]
city_array = city.values
city_array = city_array.tolist()
counts = city_count.values.tolist()

# seq用于统计每个城市中的工资
seq = 0
avg_l = []
for city_item in city_array:
    salary_list = []
    avg_list = []
    salary = pd.read_sql("select salary from lagou_table where city=\'{}\' order by city".format(city_item), conn)
    data = salary.iloc[:, 0]
    data_array = data.values
    data_array = data_array.tolist()

    for i in data_array:
        i = i.replace('k', '')
        i = i.replace('-', ' ')
        i = re.findall(r'\d+', i)
        salary_list.append(i)
    # print("城市：" + city_item)
    for s in salary_list:
        if len(s) > 1:
            avg = sum([int(a) for a in s]) / 2
        else:
            avg = int(s[0])
        avg_list.append(avg)
    # print(round(sum(avg_list) / counts[seq], 2))
    avg_l.append(round(sum(avg_list) / counts[seq], 2))
    seq += 1


# 画条形图
plt.bar(city_array, avg_l, label='平均工资')
plt.legend()
plt.xticks(rotation=45)
plt.xlabel('城市')
plt.ylabel('平均工资/K')
plt.title('全国python岗位各城市平均工资')
plt.savefig('analysisPis/avgCitySalary.png')
plt.show()
```

> * 正则表达式中
>   * `re.findall()`       返回string中所有与pattern相匹配的全部字串（返回形式为数组）
>   * `\d` 是匹配数字字符[0-9]
>   * `+` 匹配一个或多个
>   * `\d+` 是匹配一个或多个数字字符
>   * `r` 表示不转义
> * [plt.legend()](https://blog.csdn.net/helunqu2017/article/details/78641290) 用于显示图例
> * 保留两位小数
>   * `round(a,2)`
>   * `'%.2f'  %a`
>   * `Decimal('5.026').quantize(Decimal('0.00'))`
> * [条形图和直方图的区别](https://blog.csdn.net/xjl271314/article/details/80295935)
>   * `条形图` 
>       * 用条形的长度表示各类别频数的多少，其宽度（表示类别）则是固定的
>       * 横轴上的数据是孤立的，是一个具体的数据
>       * 主要用于展示分类数据
>   * `直方图`
>       * 用长方形的面积表示频数，只有当长方形的宽都相等时，才可以用长方形的高表示频数的大小，因此其高度与宽度均有意义
>       * 横轴上的数据是连续的，是一个范围
>       * 主要用于展示数据型数据

##### 全国岗位分布 地图
* mapServer.py
* maps.html
* 运行 `http://127.0.0.1:5000/maps`
###### 构造字典格式
```
import pandas as pd

information = pd.read_sql(
        "select company_full_name, latitude, longitude from lagou_table where latitude not like '0.0'", conn)
    companys = information.iloc[:, 0]
    latitude = information.iloc[:, 1]
    longtitude = information.iloc[:, 2]

    companys_list = companys.values.tolist()
    latitude_list = latitude.values.tolist()
    longtitude_list = longtitude.values.tolist()

    # zip() 函数
    data = [list(x) for x in zip(longtitude_list, latitude_list)]
    
    # 调节圆点大小
    add = ',30'
    for i in range(len(data)):
        data[i] = ','.join(data[i])
        data[i] = data[i] + add

    mix_data = [list(x) for x in zip(companys_list, data)]
    a_list = []
    for item in mix_data:
        a = {
            'name': item[0],
            
             # 将str转为list
            'value': item[1].strip(',').split(',') 
        }
        a_list.append(a)
```
###### Ajax获取后台data
```
from flask import Flask, render_template, jsonify

# 生成Flask实例
app = Flask(__name__)

@app.route('/get_data', methods=['POST'])
def get_data():
    ...
    ...
    return jsonify(a_list)


@app.route('/maps')
def maps():
    return render_template('maps.html')
    
    
if __name__ == '__main__':
    app.run()
```
```
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>

<script type="text/javascript">
    $(document).ready(function () {
        var convertData = getData();
        ...
        ...
    }
    function getData() {
        var result = null;
        //ajax
        $.ajax({
           url:'/get_data',
           type:'POST',
           async:false,
           dataType:'json',
           success:function (data) {
               result = data;
           },
           error:function (msg) {
               console.log(msg);
               alert('System Error')
           }
        });
        return result;
    }
</script>

```

[Flask](https://www.cnblogs.com/jsben/p/4909964.html)

[ECharts](http://www.echartsjs.com/examples/editor.html?c=map-polygon) 
> 需要将 `echarts.min.js` 引用放在新建的 `static` 文件下
```
<script src='../static/echarts.min.js'></script>
```
```
<!-- 使用flask的url_for -->
<!-- .py文件中需要 import url_for -->
<script src="{{ url_for('static', filename='echarts.min.js') }}"></script>
```
`zip()` 函数
* 函数用于将可迭代对象（字符串、列表、元组、字典）作为参数，将对象中对应的元素打包成一个个元组，然后返回由这些元组组成的对象

```
>>> a = [1,2,3]             #此处可迭代对象为列表
>>> b = [4,5,6]

>>> zipped = zip(a,b)
>>> zipped
<zip object at 0x02B01B48>  #返回的是一个对象

>>> list(zipped)
[(1, 4), (2, 5), (3, 6)]    #使用list()函数转换为列表
```
* 如果各个可迭代对象的元素个数不一致，则返回的对象长度与最短的可迭代对象相同
```
>>> a = [1,2,3]
>>> c = [4,5,6,7,8]

>>> list(zip(a,c))
[(1, 4), (2, 5), (3, 6)]
```
* 利用 `*` 号操作符，进行解压
```
>>> a = [1,2,3] 
>>> b = [4,5,6]

>>> zipped = zip(a,b)
>>> list(zip(*zipped))     #解压也使用list进行转换
[(1, 2, 3), (4, 5, 6)]
```
Python 中实现字符串转换为列表
* `strip()` 用于移除字符串头尾指定的字符
* `split()` 将一个字符串分裂成多个字符串组成的列表

##### 不同城市工作年限要求 Bar_Label_Rotation
* mapServer.py
* maps.html
* 运行 `http://127.0.0.1:5000/bar`
> [Left join、Right Join、Inner Join 用法](https://www.cnblogs.com/pcjim/articles/799302.html)

###### 构建 Map 格式
```
select t.city, t.work_year, count(t.id) as work_count from `lagou_table` t group by t.city, t.work_year;
```
> 根据城市和工作年限分组，统计出每个城市不同年限要求的岗位总数

```
city_datas = pd.read_sql("select city, count(city) from lagou_table group by city having count(city) > 1", conn).iloc[:, 0]
    city_list = city_datas.values.tolist()

cursor = conn.cursor()
    sql = "select t.city, t.work_year, count(t.id) as work_count from `lagou_table` t group by t.city, t.work_year"
    cursor.execute(sql)
    result = cursor.fetchall()

    city_map = {}
    for city in city_list:
        experience_count = [0] * 7
        for tp in result:
            if tp[0] == city:
                if tp[1] == '应届毕业生':
                    experience_count[0] = int(tp[2])
                elif tp[1] == '1年以下':
                    experience_count[1] = int(tp[2])
                ...
                ...

        city_map[city] = experience_count
```
> 通过两次遍历，生成 `{'上海': [38, 5, 223, 367, 68, 2, 68], '东莞': [0, 0, 5, 1, 0, 0, 0], ...}` 这种dict结构，列表默认按照工作年限从小到大的顺序

###### Ajax获取后台data
```
@app.route('/bar', methods=['GET'])
def show_map():
    return render_template('BarChart.html')
    
    
@app.route('/get_bar_data', methods=['POST'])
def get_bar_data():
    ...
    ...
    return jsonify(city_map)
```

```
var city_key = [];
var series = [];

function getData() {
               var result = null;
                //ajax
               $.ajax({
                   url:'/get_bar_data',
                   type:'POST',
                   async:false,
                   dataType:'json',
                   success:function (data) {
                       result = data;
                   },
                   error:function (msg) {
                       console.log(msg);
                       alert('System Error')
                   }
               });
               // console.log(result);
                return buildSeries(result);
           }
        
// 按照模版格式，自定义构造 json
function buildSeries(result) {

                for(var k in result){
                    city_key.push(k);
                    var map = {
                        name: k,
                        type: 'bar',
                        // label: labelOption,
                        data: result[k]
                    };
                    series.push(map)
                }
                console.log(series);
                return series;

            }
```
> * JS 获取 Map 的 key 和 value

```
//通过定义一个局部变量k遍历获取到了map中所有的key值
for(var k in map){  
    //获取到了key所对应的value的值
    var docList=map[k]; 
}
```
> * [JS 数组操作](https://www.cnblogs.com/lzm1989/p/5967815.html)
