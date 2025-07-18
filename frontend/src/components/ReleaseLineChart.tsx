import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ReactECharts from 'echarts-for-react';
import { Spin, Alert } from 'antd';

interface ReleaseLineChartProps {
  rankMin: number;
  rankMax: number;
}

interface ReleaseData {
  period: string;
  count: number;
}

const ReleaseLineChart: React.FC<ReleaseLineChartProps> = ({ rankMin, rankMax }) => {
  const [data, setData] = useState<ReleaseData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    axios
      .get('/api/release-date-distribution', {
        params: { rank_min: rankMin, rank_max: rankMax },
      })
      .then((res) => {
        if (res.data.success) {
          setData(res.data.data);
        } else {
          setError(res.data.msg || '数据获取失败');
        }
      })
      .catch((err) => {
        setError(err.message || '请求失败');
      })
      .finally(() => setLoading(false));
  }, [rankMin, rankMax]);

  const option = {
    title: {
      text: '上映时间分布',
      left: 'center',
    },
    tooltip: {
      trigger: 'axis',
    },
    xAxis: {
      type: 'category',
      data: data.map((item) => item.period),
      name: '年份区间',
    },
    yAxis: {
      type: 'value',
      name: '电影数量',
    },
    series: [
      {
        data: data.map((item) => item.count),
        type: 'line',
        smooth: true,
        name: '数量',
      },
    ],
  };

  if (loading) return <Spin tip="加载中..." />;
  if (error) return <Alert type="error" message={error} />;
  return <ReactECharts option={option} style={{ height: 400 }} />;
};

export default ReleaseLineChart;
