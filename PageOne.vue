<template>
  <div class="mainss">
  
  <div id="mallss" class="mallss" style="height: 100%;"></div>
  <div id="overlay" class="overlay">
    <!-- <div id="tests">平均值:</div> -->
  </div>
</div>
</template>
<!-- <script src="../assets/chinas"></script> -->
<!-- src\data\MenuData.js  src\api\mockServe\permission.js -->
<script>

import china from "../assets/china.json";

export default {
  data() {
    return {
      mallss:null,
    }
  },
  mounted: function () {
    // 挂载
    var _this = this // 指向this 变量作用域一致;

    // 初始化echarts图表实例
    _this.mallss = this.$echarts.init(
      document.getElementById('mallss'),
    )
    
    _this.setOption()
    // 监听窗口大小改变
    window.onresize = function () {
      // 图表自适应
      _this.mallss.resize()
     
     
      // 重新设置表格内容最大高度
      //_this.height = window.innerHeight / 2 - 140
    }
    //this.getTableData()
  },
  methods: {
    
    setOption() {
      var _this = this;
      // 调用接口
      this.$axios.all([
        this.$axios.get('http://localhost:3000/zwsd'),
        this.$axios.get('http://localhost:3000/gd'),
        this.$axios.get('http://localhost:3000/yumi'),
        this.$axios.get('http://localhost:3000/dadou'),
    
      ])
      .then(this.$axios.spread(function (res1, res2, res3, res4) {
        var data1 = res1.data;
        var data2 = res2.data;
        var data3 = res3.data;
        var data4 = res4.data;
       
      // console.log(data);
        _this.$echarts.registerMap('china', china);
        // 省份经纬度
        var geoCoordMap = {
         '新疆维吾尔自治区': [86.61 , 40.79],
         '西藏自治区':[89.13 , 30.66],
         '黑龙江省':[128.34 , 47.05],
         '吉林省':[126.32 , 43.38],
         '辽宁省':[123.42 , 41.29],
         '内蒙古自治区':[112.17 , 42.81],
         '北京市':[116.40 , 40.40 ],
         '宁夏省':[106.27 , 36.76],
         '山西省':[111.95,37.65],
         '河北省':[115.21 , 38.44],
         '天津市':[117.04 , 39.52],
         '青海省':[97.07 , 35.62],
         '甘肃省':[103.82 , 36.05],
         '山东省':[118.01 , 36.37],
         '陕西省':[108.94 , 34.46],
         '河南省':[113.46 , 34.25],
         '安徽省':[117.28 , 31.86],
         '江苏省':[120.26 , 32.54],
         '上海市':[121.46 , 31.28],
         '四川省':[103.36 , 30.65],
         '湖北省':[112.29 , 30.98],
         '浙江省':[120.15 , 29.28],
         '重庆市':[107.51 , 29.63],
         '湖南省':[112.08 , 27.79],
         '江西省':[115.89 , 27.97],
         '贵州省':[106.91 , 26.67],
         '福建省':[118.31 , 26.07],
         '云南省':[101.71 , 24.84],
         '台湾省':[121.01 , 23.54],
         '广西壮族自治区':[108.67 , 23.68],
         '广东省':[113.98 , 22.82],
         '海南省':[110.03 , 19.33],
         '澳门':[113.54 , 22.19],
         '香港':[114.17 , 22.32],
      };
      
      // 对每个地点的经纬度进行微小的随机偏移
      for (var key in geoCoordMap) {
        geoCoordMap[key][0] += getRandomOffset();
        geoCoordMap[key][1] += getRandomOffset();
      }
      // 获取一个介于 -0.005 到 0.005 之间的随机偏移量
      function getRandomOffset() {
        return (Math.random() - 0.8) * 1.1;
      }
      // 合并经纬度数据，计算平均值 
      var convertData = function (data,geoCoordMap, isTest) {
          var res = [];
          var sum=0;
          var count=0;
          for (var i = 0; i < data.length; i++) {
            var geoCoord = geoCoordMap[data[i].location];
            // 计算
            var prices  =data[i].price;
            sum = sum+prices;
            // sum+=prices;
            count++;
            console.log(sum,count);
            if (geoCoord) {
              res.push({
                name: data[i].location,
                value: geoCoord.concat(data[i].price)
              });
            }
          }
          //计算平均值
          
          var nsvg = Math.floor(sum / count);
          var textToZoom = document.createElement('p');
          textToZoom.textContent = "平均值: " + nsvg + "元/吨";
          //
          // 创建标题
          var title = document.createElement('h3');
            if (isTest === '水稻') {
              title.textContent = '水稻';
            } else if (isTest === '硬稻') {
              title.textContent = '硬稻';
            } else if (isTest === '玉米') {
              title.textContent = '玉米';
            } else if (isTest === '大豆') {
              title.textContent = '大豆';
            } else {
              title.textContent = '其他'; // 如果 data 不是上述值，则使用默认标题
            }
          textToZoom.id = 'zoomed-content'; //  ID
          overlay.appendChild(title); // 添加标题
          document.getElementById('overlay').appendChild(textToZoom); // 将动态创建的文本添加到 overlay 中
          console.log(res);
          return res;
        };
        // 分别调用函数
        var t1 = convertData(data1, geoCoordMap, "水稻");
        var t2 = convertData(data2, geoCoordMap, "硬稻");
        var t3 = convertData(data3, geoCoordMap, "玉米");
        var t4 = convertData(data4, geoCoordMap, "大豆");
        // 绘制图表
        _this.mallss.setOption({
          backgroundColor: '#111',
        title: {
            text: '中国地图',
            // subtext: '暗色主题',
            // left: 'center',
            textStyle: {
                color: '#4575b4'
            }
        },
        legend: {
          left:'35%',
          top:'20%',
          orient: 'horizontal', // 图例布局方向，'horizontal' 水平 | 'vertical' 垂直
          x: 'center', // 图例水平安放位置，默认为居中
          y: 'top', // 图例垂直安放位置，默认为顶端
          data: ['水稻', '粳稻', '玉米', '大豆'], // 图例内容（与系列名称一一对应）
          textStyle: {
            color: '#74add1', // 图例文字颜色
            fontSize: 12 // 图例文字大小
          }
        },
        tooltip: {
            
            trigger: 'item'
        },
        // visualMap: {
        //     left: "right",
        //     min: 0,
        //     max: 100,
        //     inRange: {
        //       color: [
        //         "#313695",
        //         "#4575b4",
        //         "#74add1",
        //         "#abd9e9",
        //         "#e0f3f8",
        //         "#ffffbf",
        //         "#fee090",
        //         "#fdae61",
        //         "#f46d43",
        //         "#d73027",
        //         "#a50026",
        //       ],
        //     },
        //     text: ["High", "Low"],
        //     calculable: true,
        //   },
              geo: {
                center:[108.94 , 34.46],   //[112.29 , 30.98],  //湖北为中心
                zoom:1.5,
                map: 'china',
                // left: '1%',  // 距离左侧距离占页面宽度的5%  
                // scale: 2.5,  // 按比例放大地图，这里设置为1.2表示放大20%
                roam: true,
                // regions: [
                //   {
                //     // 指定需要显示的地图区域（例如，南海诸岛的名称）
                //     name: '南海诸岛',
                //     selected: false // 设置为 false 表示隐藏该区域
                //   }
                // ],
                itemStyle: {
                  areaColor: '#e7e8ea'
              },
              itemStyle: {
                normal: {
                  areaColor: '#323c48',
                  borderColor: '#111'
                },
                emphasis: {
                  areaColor: '#2a333d'
                }
              },
        },
        series: [

                {   
                  name:'水稻',
                    type: "effectScatter",
                    coordinateSystem: "geo",
                    blendMode: 'lighter',
                    // symbolSize: function (val) {
                    //   return val[2] / 10;
                    // },
                    // tooltip: {
                    //   formatter: function (t1) {
                    //     return ': ' + t1.data[2]+'元/吨';
                    //   },
                    // },
                    encode: {
                      value: 2
                    },
                    label: {
                      formatter: '{b}',
                      position: 'right',
                      show: false
                    },
                    emphasis: {
                      label: {
                        show: true
                      }
                    },
                    itemStyle: {
                      size:'20',
                      color: '#ff7e28', // 散点颜色
                  },
                    data: t1
                },
                {
                    name:'粳稻',
                    type: "effectScatter",
                    coordinateSystem: "geo",
                    blendMode: 'lighter',
                    itemStyle: {
                      size:'20',
                      color: '#ff7a7a', // 散点颜色
                  },
                    data: t2
                },
                {
                  name:'玉米',
                    type: "effectScatter",
                    coordinateSystem: "geo",
                    blendMode: 'lighter',
                    itemStyle: {
                      size:'30',
                      color: '#afff38', // 散点颜色
                  },
                    data: t3
                },
                {
                  name:'大豆',
                    type: "effectScatter",
                    coordinateSystem: "geo",
                    itemStyle: {
                      size:'20',
                      color: '#fff238', // 散点颜色
                  },
                    data: t4
                },
            ],
        })
      }))
        }
      }
}
</script>

<style >
/* scoped="scoped" */
.mainss{
  width: 100%;
  height: 100%;
  
}
.mallss canvas{
  position: relative;
      width: 100%;
      height: 100%; 
      transform: scale(1.6);
}
.overlay {
      position: absolute;
      top: 30%;
      left: 70%;
      width: 200px;
      height: 250px;
      background-color: #666666; /* rgba(190, 188, 188, 0.742);  设置背景颜色为半透明白色 */
      z-index: 20; 
      color: #e6ff27;
      margin: 10px 10px;
      padding: 0 10px;
      /* opacity: 0.9; */
    }
    .overlay h3{
      color: rgb(225, 163, 38);
    }
.test{
  color: #24d3ff;
}
</style>