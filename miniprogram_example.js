// 小程序页面逻辑示例 (如: pages/news/news.js)

Page({
  data: {
    newsList: [],
    loading: true,
    error: null
  },

  onLoad() {
    this.fetchNews();
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.fetchNews(() => {
      wx.stopPullDownRefresh();
    });
  },

  fetchNews(callback) {
    // 替换为您在阿里云 OSS 创建的 Bucket 域名
    // 格式通常为: https://<bucket-name>.<endpoint>/news/latest.json
    // 例如: https://trend-radar-data.oss-cn-hangzhou.aliyuncs.com/news/latest.json
    const DATA_URL = 'https://YOUR_BUCKET_NAME.oss-cn-hangzhou.aliyuncs.com/news/latest.json';

    this.setData({ loading: true });

    wx.request({
      url: DATA_URL,
      method: 'GET',
      // 避免缓存，确保获取最新数据（或者可以在 URL 后加时间戳参数 ?t=Date.now()）
      header: {
        'Cache-Control': 'no-cache'
      },
      success: (res) => {
        if (res.statusCode === 200 && res.data) {
          const data = res.data;
          console.log('获取新闻成功:', data);
          
          // data.results 包含了各个平台的数据
          // 我们可以把它转换为适合列表渲染的数组
          const platforms = Object.keys(data.results).map(key => {
            return {
              id: key,
              name: data.results[key].name,
              items: data.results[key].items
            };
          });

          this.setData({
            newsList: platforms,
            updateTime: data.timestamp, // 数据生成时间
            loading: false,
            error: null
          });
        } else {
          console.error('数据格式错误:', res);
          this.setData({
            loading: false,
            error: '数据格式错误'
          });
        }
      },
      fail: (err) => {
        console.error('请求失败:', err);
        this.setData({
          loading: false,
          error: '网络请求失败，请稍后重试'
        });
      },
      complete: () => {
        if (callback) callback();
      }
    });
  }
});
